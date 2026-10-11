import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.database.session import Base

class UploadedDataset(Base):
    __tablename__ = 'uploaded_datasets'
    
    id = Column(String(36), primary_key=True)
    filename = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)
    row_count = Column(Integer, nullable=False)
    column_count = Column(Integer, nullable=False)
    columns_json = Column(Text, nullable=False)
    preview_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    runs = relationship('DetectionRun', back_populates='dataset', cascade='all, delete-orphan')

class DetectionRun(Base):
    __tablename__ = 'detection_runs'
    
    id = Column(String(36), primary_key=True)
    dataset_id = Column(String(36), ForeignKey('uploaded_datasets.id', ondelete='SET NULL'), nullable=True)
    dataset_name = Column(String(255), nullable=False)
    model_name = Column(String(100), nullable=False)
    total_records = Column(Integer, nullable=False)
    normal_count = Column(Integer, nullable=False)
    anomaly_count = Column(Integer, nullable=False)
    anomaly_percentage = Column(Float, nullable=False)
    duration_ms = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), default='completed')
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    
    dataset = relationship('UploadedDataset', back_populates='runs')
    predictions = relationship('TrafficPrediction', back_populates='run', cascade='all, delete-orphan')
    alerts = relationship('SecurityAlert', back_populates='run', cascade='all, delete-orphan')

class TrafficPrediction(Base):
    __tablename__ = 'traffic_predictions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(36), ForeignKey('detection_runs.id', ondelete='CASCADE'), nullable=False, index=True)
    record_index = Column(Integer, nullable=False)
    destination_port = Column(Integer, nullable=False, index=True)
    flow_duration = Column(Float, nullable=False)
    total_fwd_packets = Column(Integer, nullable=False)
    total_backward_packets = Column(Integer, nullable=False)
    total_fwd_len = Column(Float, nullable=False)
    total_bwd_len = Column(Float, nullable=False)
    fwd_pkt_len_max = Column(Float, nullable=False)
    fwd_pkt_len_min = Column(Float, nullable=False)
    fwd_pkt_len_mean = Column(Float, nullable=False)
    fwd_pkt_len_std = Column(Float, nullable=False)
    true_label = Column(String(100), nullable=True)
    predicted_label = Column(String(100), nullable=False, index=True)
    is_anomaly = Column(Boolean, nullable=False, index=True)
    anomaly_score = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    severity = Column(String(50), nullable=False, default='low', index=True)
    raw_features_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    run = relationship('DetectionRun', back_populates='predictions')
    alert = relationship('SecurityAlert', back_populates='prediction', uselist=False)

class SecurityAlert(Base):
    __tablename__ = 'security_alerts'
    
    id = Column(String(36), primary_key=True)
    run_id = Column(String(36), ForeignKey('detection_runs.id', ondelete='CASCADE'), nullable=False, index=True)
    prediction_id = Column(Integer, ForeignKey('traffic_predictions.id', ondelete='CASCADE'), nullable=True)
    record_index = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    alert_title = Column(String(255), nullable=False)
    attack_category = Column(String(100), nullable=False, index=True)
    severity = Column(String(50), nullable=False, index=True) # critical, high, medium, low
    destination_port = Column(Integer, nullable=False)
    evidence_summary = Column(Text, nullable=False)
    investigation_status = Column(String(50), default='New', index=True) # New, Investigating, Resolved
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    run = relationship('DetectionRun', back_populates='alerts')
    prediction = relationship('TrafficPrediction', back_populates='alert')

class ModelEvaluation(Base):
    __tablename__ = 'model_evaluations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String(100), nullable=False)
    model_type = Column(String(50), nullable=False) # Supervised, Unsupervised
    accuracy = Column(Float, nullable=False)
    precision = Column(Float, nullable=False)
    recall = Column(Float, nullable=False)
    f1_score = Column(Float, nullable=False)
    roc_auc = Column(Float, nullable=True)
    fpr = Column(Float, nullable=True)
    confusion_matrix_json = Column(Text, nullable=False)
    class_report_json = Column(Text, nullable=True)
    trained_at = Column(DateTime, default=datetime.datetime.utcnow)

class ChatSession(Base):
    __tablename__ = 'chat_sessions'
    
    id = Column(String(36), primary_key=True)
    title = Column(String(255), default='Cyber Defense Session')
    active_run_id = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    messages = relationship('ChatMessage', back_populates='session', cascade='all, delete-orphan')

class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(36), ForeignKey('chat_sessions.id', ondelete='CASCADE'), nullable=False, index=True)
    role = Column(String(50), nullable=False) # user, assistant
    content = Column(Text, nullable=False)
    context_run_id = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    session = relationship('ChatSession', back_populates='messages')
