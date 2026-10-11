import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import SecurityAlert, DetectionRun
from app.schemas.schemas import AlertUpdateRequest

router = APIRouter(prefix='/alerts', tags=['Security Alerts'])

@router.get('')
def get_alerts(
    run_id: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(SecurityAlert)
    
    if run_id:
        query = query.filter(SecurityAlert.run_id == run_id)
        
    if severity and severity != 'all':
        query = query.filter(SecurityAlert.severity == severity.lower())
        
    if status and status != 'all':
        query = query.filter(SecurityAlert.investigation_status == status)
        
    if search:
        search_fmt = f'%{search}%'
        query = query.filter(
            (SecurityAlert.alert_title.ilike(search_fmt)) |
            (SecurityAlert.attack_category.ilike(search_fmt)) |
            (SecurityAlert.evidence_summary.ilike(search_fmt))
        )
        
    total = query.count()
    offset = (page - 1) * page_size
    alerts = query.order_by(SecurityAlert.timestamp.desc()).offset(offset).limit(page_size).all()
    total_pages = (total + page_size - 1) // page_size if total > 0 else 0
    
    return {
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': total_pages,
        'alerts': [
            {
                'id': a.id,
                'run_id': a.run_id,
                'prediction_id': a.prediction_id,
                'record_index': a.record_index,
                'timestamp': a.timestamp,
                'alert_title': a.alert_title,
                'attack_category': a.attack_category,
                'severity': a.severity,
                'destination_port': a.destination_port,
                'evidence_summary': a.evidence_summary,
                'investigation_status': a.investigation_status,
                'notes': a.notes,
                'created_at': a.created_at,
                'updated_at': a.updated_at
            }
            for a in alerts
        ]
    }

@router.get('/{alert_id}')
def get_alert_detail(alert_id: str, db: Session = Depends(get_db)):
    alert = db.query(SecurityAlert).filter(SecurityAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail='Alert not found.')
    return {
        'id': alert.id,
        'run_id': alert.run_id,
        'prediction_id': alert.prediction_id,
        'record_index': alert.record_index,
        'timestamp': alert.timestamp,
        'alert_title': alert.alert_title,
        'attack_category': alert.attack_category,
        'severity': alert.severity,
        'destination_port': alert.destination_port,
        'evidence_summary': alert.evidence_summary,
        'investigation_status': alert.investigation_status,
        'notes': alert.notes,
        'created_at': alert.created_at,
        'updated_at': alert.updated_at
    }

@router.patch('/{alert_id}')
def update_alert(alert_id: str, update_data: AlertUpdateRequest, db: Session = Depends(get_db)):
    alert = db.query(SecurityAlert).filter(SecurityAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail='Alert not found.')
        
    if update_data.investigation_status is not None:
        if update_data.investigation_status not in ['New', 'Investigating', 'Resolved']:
            raise HTTPException(status_code=400, detail='Invalid status. Must be New, Investigating, or Resolved.')
        alert.investigation_status = update_data.investigation_status
        
    if update_data.notes is not None:
        alert.notes = update_data.notes
        
    alert.updated_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(alert)
    
    return {
        'id': alert.id,
        'investigation_status': alert.investigation_status,
        'notes': alert.notes,
        'updated_at': alert.updated_at
    }
