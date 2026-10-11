import json
from collections import Counter
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.session import get_db
from app.database.models import DetectionRun, TrafficPrediction, SecurityAlert

router = APIRouter(prefix='/dashboard', tags=['Dashboard'])

@router.get('/summary')
def get_dashboard_summary(run_id: str = Query(None), db: Session = Depends(get_db)):
    if not run_id:
        latest = db.query(DetectionRun).order_by(DetectionRun.created_at.desc()).first()
    else:
        latest = db.query(DetectionRun).filter(DetectionRun.id == run_id).first()
        
    if not latest:
        return {
            'total_analyzed': 0,
            'normal_count': 0,
            'anomaly_count': 0,
            'anomaly_percentage': 0.0,
            'active_alerts_count': 0,
            'critical_alerts_count': 0,
            'model_in_use': 'Random Forest Classifier',
            'latest_run_id': None,
            'class_distribution': {},
            'severity_distribution': {},
            'top_attack_ports': []
        }
        
    # Active alerts
    active_alerts = db.query(SecurityAlert).filter(
        SecurityAlert.run_id == latest.id,
        SecurityAlert.investigation_status != 'Resolved'
    ).count()
    
    critical_alerts = db.query(SecurityAlert).filter(
        SecurityAlert.run_id == latest.id,
        SecurityAlert.severity == 'critical'
    ).count()
    
    # Class distribution
    preds = db.query(TrafficPrediction.predicted_label, func.count(TrafficPrediction.id)).filter(
        TrafficPrediction.run_id == latest.id
    ).group_by(TrafficPrediction.predicted_label).all()
    class_dist = {cls: count for cls, count in preds}
    
    # Severity distribution
    sevs = db.query(TrafficPrediction.severity, func.count(TrafficPrediction.id)).filter(
        TrafficPrediction.run_id == latest.id
    ).group_by(TrafficPrediction.severity).all()
    sev_dist = {s: count for s, count in sevs}
    
    # Top attack ports
    attack_ports = db.query(
        TrafficPrediction.destination_port,
        func.count(TrafficPrediction.id).label('cnt')
    ).filter(
        TrafficPrediction.run_id == latest.id,
        TrafficPrediction.is_anomaly == True
    ).group_by(TrafficPrediction.destination_port).order_by(func.count(TrafficPrediction.id).desc()).limit(6).all()
    
    port_list = [{'port': p[0], 'count': p[1]} for p in attack_ports]
    
    return {
        'total_analyzed': latest.total_records,
        'normal_count': latest.normal_count,
        'anomaly_count': latest.anomaly_count,
        'anomaly_percentage': latest.anomaly_percentage,
        'active_alerts_count': active_alerts,
        'critical_alerts_count': critical_alerts,
        'model_in_use': latest.model_name,
        'latest_run_id': latest.id,
        'created_at': latest.created_at,
        'class_distribution': class_dist,
        'severity_distribution': sev_dist,
        'top_attack_ports': port_list
    }

@router.get('/trends')
def get_dashboard_trends(run_id: str = Query(None), db: Session = Depends(get_db)):
    if not run_id:
        latest = db.query(DetectionRun).order_by(DetectionRun.created_at.desc()).first()
    else:
        latest = db.query(DetectionRun).filter(DetectionRun.id == run_id).first()
        
    if not latest:
        return {
            'port_distribution': [],
            'duration_distribution': [],
            'anomaly_score_bins': [],
            'attack_breakdown': []
        }
        
    preds = db.query(TrafficPrediction).filter(TrafficPrediction.run_id == latest.id).all()
    
    # Port distribution: top ports with normal vs anomaly breakdown
    port_counts = {}
    for p in preds:
        port = p.destination_port
        if port not in port_counts:
            port_counts[port] = {'port': port, 'normal': 0, 'anomaly': 0, 'total': 0}
        if p.is_anomaly:
            port_counts[port]['anomaly'] += 1
        else:
            port_counts[port]['normal'] += 1
        port_counts[port]['total'] += 1
        
    sorted_ports = sorted(port_counts.values(), key=lambda x: x['total'], reverse=True)[:8]
    
    # Duration bins
    durations = [p.flow_duration for p in preds]
    # define logarithmic/practical bins
    dur_bins = [
        {'range': '< 1ms', 'count': 0},
        {'range': '1ms - 100ms', 'count': 0},
        {'range': '100ms - 1s', 'count': 0},
        {'range': '1s - 10s', 'count': 0},
        {'range': '> 10s', 'count': 0}
    ]
    for d in durations:
        # duration in dataset is in microseconds
        ms = d / 1000.0
        if ms < 1.0:
            dur_bins[0]['count'] += 1
        elif ms <= 100.0:
            dur_bins[1]['count'] += 1
        elif ms <= 1000.0:
            dur_bins[2]['count'] += 1
        elif ms <= 10000.0:
            dur_bins[3]['count'] += 1
        else:
            dur_bins[4]['count'] += 1
            
    # Anomaly score distribution bins
    score_bins = [
        {'bin': '0.0 - 0.2', 'count': 0},
        {'bin': '0.2 - 0.4', 'count': 0},
        {'bin': '0.4 - 0.6', 'count': 0},
        {'bin': '0.6 - 0.8', 'count': 0},
        {'bin': '0.8 - 1.0', 'count': 0}
    ]
    for p in preds:
        s = p.confidence if p.confidence is not None else p.anomaly_score
        if s < 0.2:
            score_bins[0]['count'] += 1
        elif s < 0.4:
            score_bins[1]['count'] += 1
        elif s < 0.6:
            score_bins[2]['count'] += 1
        elif s < 0.8:
            score_bins[3]['count'] += 1
        else:
            score_bins[4]['count'] += 1
            
    # Attack breakdown
    attack_counter = Counter([p.predicted_label for p in preds if p.is_anomaly])
    attack_breakdown = [{'name': k, 'value': v} for k, v in attack_counter.items()]
    
    return {
        'port_distribution': sorted_ports,
        'duration_distribution': dur_bins,
        'anomaly_score_bins': score_bins,
        'attack_breakdown': attack_breakdown
    }
