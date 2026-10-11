import os
import time
import uuid
import json
import pandas as pd
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import DetectionRun, TrafficPrediction, SecurityAlert, UploadedDataset
from app.ml.predictor import predict_dataframe
from app.core.config import settings

router = APIRouter(prefix='/detection', tags=['Detection'])

@router.post('/analyze')
async def analyze_traffic(
    file: Optional[UploadFile] = File(None),
    dataset_id: Optional[str] = Form(None),
    model_type: str = Form('random_forest'), # 'random_forest' or 'isolation_forest'
    db: Session = Depends(get_db)
):
    start_time = time.time()
    df = None
    dataset_name = 'CIC-IDS2017.xlsx'
    matched_dataset_id = None
    
    if file and file.filename:
        filename = file.filename
        content = await file.read()
        dataset_name = filename
        if filename.endswith('.csv'):
            import io
            df = pd.read_csv(io.BytesIO(content))
        else:
            import io
            df = pd.read_excel(io.BytesIO(content))
    elif dataset_id:
        ds_record = db.query(UploadedDataset).filter(UploadedDataset.id == dataset_id).first()
        if ds_record:
            matched_dataset_id = ds_record.id
            dataset_name = ds_record.filename
            file_candidates = [
                os.path.join(settings.DATASETS_DIR, f'{ds_record.id}_{ds_record.filename}'),
                os.path.join(settings.DATASETS_DIR, ds_record.filename),
                os.path.join(os.path.dirname(settings.DATASETS_DIR), ds_record.filename)
            ]
            for fc in file_candidates:
                if os.path.exists(fc):
                    df = pd.read_csv(fc) if fc.endswith('.csv') else pd.read_excel(fc)
                    break
        if df is None:
            # Fallback to standard dataset
            default_path = os.path.join(os.path.dirname(settings.DATASETS_DIR), 'CIC-IDS2017.xlsx')
            if os.path.exists(default_path):
                df = pd.read_excel(default_path)
                dataset_name = 'CIC-IDS2017.xlsx'
    else:
        # Default to root CIC-IDS2017.xlsx
        default_path = os.path.join(os.path.dirname(settings.DATASETS_DIR), 'CIC-IDS2017.xlsx')
        if not os.path.exists(default_path):
            default_path = os.path.join(settings.DATASETS_DIR, 'CIC-IDS2017.xlsx')
        if os.path.exists(default_path):
            df = pd.read_excel(default_path)
            dataset_name = 'CIC-IDS2017.xlsx'
        else:
            raise HTTPException(status_code=400, detail='No dataset provided and default CIC-IDS2017.xlsx not found.')
            
    if df is None or len(df) == 0:
        raise HTTPException(status_code=400, detail='Dataset is empty or could not be loaded.')
        
    try:
        results = predict_dataframe(df, model_type=model_type)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'ML Inference failed: {str(e)}')
        
    duration_ms = round((time.time() - start_time) * 1000.0, 2)
    run_id = str(uuid.uuid4())
    
    detection_run = DetectionRun(
        id=run_id,
        dataset_id=matched_dataset_id,
        dataset_name=dataset_name,
        model_name='Random Forest Classifier' if model_type == 'random_forest' else 'Isolation Forest',
        total_records=results['total_records'],
        normal_count=results['normal_count'],
        anomaly_count=results['anomaly_count'],
        anomaly_percentage=results['anomaly_percentage'],
        duration_ms=duration_ms,
        status='completed'
    )
    db.add(detection_run)
    db.flush()
    
    # Batch insert predictions and generate security alerts
    prediction_objs = []
    alert_objs = []
    
    for r in results['records']:
        pred = TrafficPrediction(
            run_id=run_id,
            record_index=r['record_index'],
            destination_port=r['destination_port'],
            flow_duration=r['flow_duration'],
            total_fwd_packets=r['total_fwd_packets'],
            total_backward_packets=r['total_backward_packets'],
            total_fwd_len=r['total_fwd_len'],
            total_bwd_len=r['total_bwd_len'],
            fwd_pkt_len_max=r['fwd_pkt_len_max'],
            fwd_pkt_len_min=r['fwd_pkt_len_min'],
            fwd_pkt_len_mean=r['fwd_pkt_len_mean'],
            fwd_pkt_len_std=r['fwd_pkt_len_std'],
            true_label=r['true_label'],
            predicted_label=r['predicted_label'],
            is_anomaly=r['is_anomaly'],
            anomaly_score=r['anomaly_score'],
            confidence=r['confidence'],
            severity=r['severity'],
            raw_features_json=json.dumps(r['raw_features'])
        )
        prediction_objs.append(pred)
        
    db.bulk_save_objects(prediction_objs, return_defaults=True)
    db.flush()
    
    # Query inserted predictions to link alerts
    inserted_preds = db.query(TrafficPrediction).filter(TrafficPrediction.run_id == run_id).all()
    for pred in inserted_preds:
        if pred.is_anomaly or pred.severity in ['critical', 'high']:
            alert_id = str(uuid.uuid4())
            port = pred.destination_port
            label = pred.predicted_label
            dur = pred.flow_duration
            tot_pkts = pred.total_fwd_packets + pred.total_backward_packets
            
            title = f'{label} Detected on Port {port}'
            evidence = (
                f'Signature: {label}. Target port: {port}. '
                f'Packets: {tot_pkts} (Fwd: {pred.total_fwd_packets}, Bwd: {pred.total_backward_packets}). '
                f'Flow Duration: {dur:,.0f} us. Model Confidence/Score: {pred.confidence:.2%}.'
            )
            
            alert = SecurityAlert(
                id=alert_id,
                run_id=run_id,
                prediction_id=pred.id,
                record_index=pred.record_index,
                alert_title=title,
                attack_category=label,
                severity=pred.severity,
                destination_port=port,
                evidence_summary=evidence,
                investigation_status='New',
                notes=None
            )
            alert_objs.append(alert)
            
    if alert_objs:
        db.bulk_save_objects(alert_objs)
        
    db.commit()
    
    return {
        'id': detection_run.id,
        'dataset_name': detection_run.dataset_name,
        'model_name': detection_run.model_name,
        'total_records': detection_run.total_records,
        'normal_count': detection_run.normal_count,
        'anomaly_count': detection_run.anomaly_count,
        'anomaly_percentage': detection_run.anomaly_percentage,
        'duration_ms': detection_run.duration_ms,
        'alerts_count': len(alert_objs),
        'status': detection_run.status,
        'created_at': detection_run.created_at
    }

@router.get('/results')
def get_detection_results(
    run_id: Optional[str] = Query(None),
    is_anomaly: Optional[str] = Query(None), # 'all', 'true', 'false'
    severity: Optional[str] = Query(None),
    predicted_label: Optional[str] = Query(None),
    port: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=200),
    db: Session = Depends(get_db)
):
    if not run_id:
        latest = db.query(DetectionRun).order_by(DetectionRun.created_at.desc()).first()
        if not latest:
            return {'run_id': '', 'total': 0, 'page': page, 'page_size': page_size, 'total_pages': 0, 'records': []}
        run_id = latest.id
        
    query = db.query(TrafficPrediction).filter(TrafficPrediction.run_id == run_id)
    
    if is_anomaly == 'true':
        query = query.filter(TrafficPrediction.is_anomaly == True)
    elif is_anomaly == 'false':
        query = query.filter(TrafficPrediction.is_anomaly == False)
        
    if severity and severity != 'all':
        query = query.filter(TrafficPrediction.severity == severity.lower())
        
    if predicted_label and predicted_label != 'all':
        query = query.filter(TrafficPrediction.predicted_label == predicted_label)
        
    if port:
        query = query.filter(TrafficPrediction.destination_port == port)
        
    if search:
        search_fmt = f'%{search}%'
        query = query.filter(
            (TrafficPrediction.predicted_label.ilike(search_fmt)) |
            (TrafficPrediction.true_label.ilike(search_fmt))
        )
        
    total = query.count()
    offset = (page - 1) * page_size
    records = query.order_by(TrafficPrediction.record_index.asc()).offset(offset).limit(page_size).all()
    total_pages = (total + page_size - 1) // page_size if total > 0 else 0
    
    return {
        'run_id': run_id,
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': total_pages,
        'records': [
            {
                'id': r.id,
                'record_index': r.record_index,
                'destination_port': r.destination_port,
                'flow_duration': r.flow_duration,
                'total_fwd_packets': r.total_fwd_packets,
                'total_backward_packets': r.total_backward_packets,
                'total_fwd_len': r.total_fwd_len,
                'total_bwd_len': r.total_bwd_len,
                'fwd_pkt_len_max': r.fwd_pkt_len_max,
                'fwd_pkt_len_min': r.fwd_pkt_len_min,
                'fwd_pkt_len_mean': r.fwd_pkt_len_mean,
                'fwd_pkt_len_std': r.fwd_pkt_len_std,
                'true_label': r.true_label,
                'predicted_label': r.predicted_label,
                'is_anomaly': r.is_anomaly,
                'anomaly_score': r.anomaly_score,
                'confidence': r.confidence,
                'severity': r.severity,
                'raw_features': json.loads(r.raw_features_json) if r.raw_features_json else None
            }
            for r in records
        ]
    }

@router.get('/results/{record_id}')
def get_single_record(record_id: int, db: Session = Depends(get_db)):
    pred = db.query(TrafficPrediction).filter(TrafficPrediction.id == record_id).first()
    if not pred:
        raise HTTPException(status_code=404, detail='Record not found.')
    return {
        'id': pred.id,
        'run_id': pred.run_id,
        'record_index': pred.record_index,
        'destination_port': pred.destination_port,
        'flow_duration': pred.flow_duration,
        'total_fwd_packets': pred.total_fwd_packets,
        'total_backward_packets': pred.total_backward_packets,
        'total_fwd_len': pred.total_fwd_len,
        'total_bwd_len': pred.total_bwd_len,
        'fwd_pkt_len_max': pred.fwd_pkt_len_max,
        'fwd_pkt_len_min': pred.fwd_pkt_len_min,
        'fwd_pkt_len_mean': pred.fwd_pkt_len_mean,
        'fwd_pkt_len_std': pred.fwd_pkt_len_std,
        'true_label': pred.true_label,
        'predicted_label': pred.predicted_label,
        'is_anomaly': pred.is_anomaly,
        'anomaly_score': pred.anomaly_score,
        'confidence': pred.confidence,
        'severity': pred.severity,
        'raw_features': json.loads(pred.raw_features_json) if pred.raw_features_json else None
    }
