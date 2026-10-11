import io
import csv
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import DetectionRun, TrafficPrediction, SecurityAlert

router = APIRouter(tags=['History and Reports'])

@router.get('/history')
def get_analysis_history(db: Session = Depends(get_db)):
    runs = db.query(DetectionRun).order_by(DetectionRun.created_at.desc()).all()
    res = []
    for r in runs:
        alerts_count = db.query(SecurityAlert).filter(SecurityAlert.run_id == r.id).count()
        res.append({
            'id': r.id,
            'dataset_name': r.dataset_name,
            'model_name': r.model_name,
            'total_records': r.total_records,
            'normal_count': r.normal_count,
            'anomaly_count': r.anomaly_count,
            'anomaly_percentage': r.anomaly_percentage,
            'duration_ms': r.duration_ms,
            'status': r.status,
            'created_at': r.created_at,
            'alerts_count': alerts_count
        })
    return res

@router.get('/reports/export')
def export_report_csv(run_id: str = Query(...), db: Session = Depends(get_db)):
    run = db.query(DetectionRun).filter(DetectionRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail='Detection run not found.')
        
    preds = db.query(TrafficPrediction).filter(TrafficPrediction.run_id == run_id).order_by(TrafficPrediction.record_index.asc()).all()
    if not preds:
        raise HTTPException(status_code=404, detail='No predictions found for this run.')
        
    output = io.StringIO()
    writer = csv.writer(output)
    
    headers = [
        'Record Index', 'Destination Port', 'Flow Duration (us)',
        'Total Fwd Packets', 'Total Backward Packets',
        'Total Fwd Length', 'Total Bwd Length',
        'Fwd Pkt Len Max', 'Fwd Pkt Len Min', 'Fwd Pkt Len Mean', 'Fwd Pkt Len Std',
        'True Label', 'Predicted Label', 'Is Anomaly', 'Confidence / Score', 'Severity'
    ]
    writer.writerow(headers)
    
    for p in preds:
        writer.writerow([
            p.record_index,
            p.destination_port,
            p.flow_duration,
            p.total_fwd_packets,
            p.total_backward_packets,
            p.total_fwd_len,
            p.total_bwd_len,
            p.fwd_pkt_len_max,
            p.fwd_pkt_len_min,
            p.fwd_pkt_len_mean,
            p.fwd_pkt_len_std,
            p.true_label or 'N/A',
            p.predicted_label,
            'YES' if p.is_anomaly else 'NO',
            round(p.confidence, 4),
            p.severity.upper()
        ])
        
    output.seek(0)
    filename = f"NetGuard_Analysis_{run_id[:8]}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
