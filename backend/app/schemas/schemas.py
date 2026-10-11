from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict
import datetime

class BaseSchema(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

class DatasetPreviewResponse(BaseSchema):
    filename: str
    file_size: int
    row_count: int
    column_count: int
    columns: List[str]
    canonical_mapped: Dict[str, str]
    is_valid: bool
    missing_required: List[str]
    preview_records: List[Dict[str, Any]]

class AnalyzeRequest(BaseSchema):
    dataset_id: Optional[str] = None
    model_type: str = "random_forest"

class PredictionRecord(BaseSchema):
    id: Optional[int] = None
    record_index: int
    destination_port: int
    flow_duration: float
    total_fwd_packets: int
    total_backward_packets: int
    total_fwd_len: float
    total_bwd_len: float
    fwd_pkt_len_max: float
    fwd_pkt_len_min: float
    fwd_pkt_len_mean: float
    fwd_pkt_len_std: float
    true_label: Optional[str] = None
    predicted_label: str
    is_anomaly: bool
    anomaly_score: float
    confidence: float
    severity: str
    raw_features: Optional[Dict[str, float]] = None

class DetectionRunResponse(BaseSchema):
    id: str
    dataset_name: str
    model_name: str
    total_records: int
    normal_count: int
    anomaly_count: int
    anomaly_percentage: float
    duration_ms: float
    status: str
    created_at: datetime.datetime
    alerts_count: int

class DetectionResultsPage(BaseSchema):
    run_id: str
    total: int
    page: int
    page_size: int
    total_pages: int
    records: List[PredictionRecord]

class DashboardSummaryResponse(BaseSchema):
    total_analyzed: int
    normal_count: int
    anomaly_count: int
    anomaly_percentage: float
    active_alerts_count: int
    critical_alerts_count: int
    model_in_use: str
    latest_run_id: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
    class_distribution: Dict[str, int]
    severity_distribution: Dict[str, int]
    top_attack_ports: List[Dict[str, Any]]

class DashboardTrendsResponse(BaseSchema):
    port_distribution: List[Dict[str, Any]]
    duration_distribution: List[Dict[str, Any]]
    anomaly_score_bins: List[Dict[str, Any]]
    attack_breakdown: List[Dict[str, Any]]

class SecurityAlertResponse(BaseSchema):
    id: str
    run_id: str
    prediction_id: Optional[int]
    record_index: int
    timestamp: datetime.datetime
    alert_title: str
    attack_category: str
    severity: str
    destination_port: int
    evidence_summary: str
    investigation_status: str
    notes: Optional[str] = None

class AlertUpdateRequest(BaseSchema):
    investigation_status: Optional[str] = None
    notes: Optional[str] = None

class ModelMetricResponse(BaseSchema):
    model_name: str
    type: str
    test_accuracy: float
    test_precision: float
    test_recall: float
    test_f1: float
    false_positive_rate: Optional[float] = None
    roc_auc: Optional[float] = None
    confusion_matrix: Dict[str, Any]
    feature_importances: Optional[Dict[str, float]] = None
    classification_report: Optional[Dict[str, Any]] = None

class ChatRequest(BaseSchema):
    message: str
    session_id: Optional[str] = None
    run_id: Optional[str] = None
    record_index: Optional[int] = None

class ChatResponse(BaseSchema):
    response: str
    session_id: str
    grounded_stats: Optional[Dict[str, Any]] = None
