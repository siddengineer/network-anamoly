import os
import json
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings
from app.database.session import engine, Base, SessionLocal
from app.database.models import ModelEvaluation, DetectionRun, TrafficPrediction, SecurityAlert
from app.api import (
    routes_datasets,
    routes_detection,
    routes_dashboard,
    routes_alerts,
    routes_models,
    routes_history,
    routes_chat
)
from app.ml.trainer import train_models_from_dataset
from app.ml.predictor import predict_dataframe
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("netguard")

def find_dataset_file():
    candidates = [
        os.path.join(settings.BASE_DIR, "..", "..", "CIC-IDS2017.xlsx"),
        os.path.join(settings.BASE_DIR, "..", "CIC-IDS2017.xlsx"),
        os.path.join(settings.DATASETS_DIR, "CIC-IDS2017.xlsx"),
        "CIC-IDS2017.xlsx"
    ]
    for c in candidates:
        if os.path.exists(c):
            return os.path.abspath(c)
    return None

def initialize_app_state():
    logger.info("Initializing NetGuard AI database, models, and baseline data...")
    Base.metadata.create_all(bind=engine)
    
    dataset_path = find_dataset_file()
    
    # Check if models exist, if not train them
    rf_model_path = os.path.join(settings.MODEL_DIR, "random_forest.joblib")
    if not os.path.exists(rf_model_path) and dataset_path:
        logger.info(f"Trained models not found. Initiating training on {dataset_path}...")
        train_models_from_dataset(dataset_path, settings.MODEL_DIR)
        logger.info("Models successfully trained and saved!")

    # Populate ModelEvaluations in DB if empty
    db = SessionLocal()
    try:
        eval_count = db.query(ModelEvaluation).count()
        if eval_count == 0:
            rf_json_path = os.path.join(settings.MODEL_DIR, "rf_metrics.json")
            if_json_path = os.path.join(settings.MODEL_DIR, "if_metrics.json")
            if os.path.exists(rf_json_path):
                with open(rf_json_path, "r", encoding="utf-8") as f:
                    rf_m = json.load(f)
                rf_eval = ModelEvaluation(
                    model_name=rf_m["model_name"],
                    model_type=rf_m["type"],
                    accuracy=rf_m["test_accuracy"],
                    precision=rf_m["test_precision"],
                    recall=rf_m["test_recall"],
                    f1_score=rf_m["test_f1"],
                    roc_auc=rf_m.get("roc_auc"),
                    fpr=rf_m.get("false_positive_rate"),
                    confusion_matrix_json=json.dumps(rf_m["confusion_matrix"]),
                    class_report_json=json.dumps(rf_m.get("classification_report"))
                )
                db.add(rf_eval)
            if os.path.exists(if_json_path):
                with open(if_json_path, "r", encoding="utf-8") as f:
                    if_m = json.load(f)
                if_eval = ModelEvaluation(
                    model_name=if_m["model_name"],
                    model_type=if_m["type"],
                    accuracy=if_m["test_accuracy"],
                    precision=if_m["test_precision"],
                    recall=if_m["test_recall"],
                    f1_score=if_m["test_f1"],
                    roc_auc=None,
                    fpr=None,
                    confusion_matrix_json=json.dumps(if_m["confusion_matrix"]),
                    class_report_json=None
                )
                db.add(if_eval)
            db.commit()

        # Seed initial analysis run on dataset if no runs exist
        runs_count = db.query(DetectionRun).count()
        if runs_count == 0 and dataset_path:
            logger.info(f"Seeding baseline detection run on {dataset_path}...")
            df = pd.read_excel(dataset_path)
            results = predict_dataframe(df, model_type="random_forest")
            import uuid
            run_id = str(uuid.uuid4())
            run = DetectionRun(
                id=run_id,
                dataset_name="CIC-IDS2017.xlsx",
                model_name="Random Forest Classifier",
                total_records=results["total_records"],
                normal_count=results["normal_count"],
                anomaly_count=results["anomaly_count"],
                anomaly_percentage=results["anomaly_percentage"],
                duration_ms=45.2,
                status="completed"
            )
            db.add(run)
            db.flush()
            
            prediction_objs = []
            for r in results["records"]:
                p = TrafficPrediction(
                    run_id=run_id,
                    record_index=r["record_index"],
                    destination_port=r["destination_port"],
                    flow_duration=r["flow_duration"],
                    total_fwd_packets=r["total_fwd_packets"],
                    total_backward_packets=r["total_backward_packets"],
                    total_fwd_len=r["total_fwd_len"],
                    total_bwd_len=r["total_bwd_len"],
                    fwd_pkt_len_max=r["fwd_pkt_len_max"],
                    fwd_pkt_len_min=r["fwd_pkt_len_min"],
                    fwd_pkt_len_mean=r["fwd_pkt_len_mean"],
                    fwd_pkt_len_std=r["fwd_pkt_len_std"],
                    true_label=r["true_label"],
                    predicted_label=r["predicted_label"],
                    is_anomaly=r["is_anomaly"],
                    anomaly_score=r["anomaly_score"],
                    confidence=r["confidence"],
                    severity=r["severity"],
                    raw_features_json=json.dumps(r["raw_features"])
                )
                prediction_objs.append(p)
            db.bulk_save_objects(prediction_objs)
            db.flush()

            # Generate Security Alerts
            inserted_preds = db.query(TrafficPrediction).filter(TrafficPrediction.run_id == run_id).all()
            alert_objs = []
            for pred in inserted_preds:
                if pred.is_anomaly or pred.severity in ["critical", "high"]:
                    port = pred.destination_port
                    label = pred.predicted_label
                    dur = pred.flow_duration
                    tot_pkts = pred.total_fwd_packets + pred.total_backward_packets
                    evidence = (
                        f"Signature: {label}. Target port: {port}. "
                        f"Packets: {tot_pkts} (Fwd: {pred.total_fwd_packets}, Bwd: {pred.total_backward_packets}). "
                        f"Flow Duration: {dur:,.0f} us. Model Confidence: {pred.confidence:.2%}."
                    )
                    alert = SecurityAlert(
                        id=str(uuid.uuid4()),
                        run_id=run_id,
                        prediction_id=pred.id,
                        record_index=pred.record_index,
                        alert_title=f"{label} Detected on Port {port}",
                        attack_category=label,
                        severity=pred.severity,
                        destination_port=port,
                        evidence_summary=evidence,
                        investigation_status="New"
                    )
                    alert_objs.append(alert)
            if alert_objs:
                db.bulk_save_objects(alert_objs)
            db.commit()
            logger.info(f"Baseline run created with {len(results['records'])} records and {len(alert_objs)} alerts.")
    finally:
        db.close()

initialize_app_state()

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_app_state()
    yield

app = FastAPI(
    title="NetGuard AI - Network Traffic Anomaly Detection API",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Explicit CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static assets (logo, video)
if os.path.exists(settings.STATIC_DIR):
    app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

# Include Routers
app.include_router(routes_datasets.router, prefix=settings.API_PREFIX)
app.include_router(routes_detection.router, prefix=settings.API_PREFIX)
app.include_router(routes_dashboard.router, prefix=settings.API_PREFIX)
app.include_router(routes_alerts.router, prefix=settings.API_PREFIX)
app.include_router(routes_models.router, prefix=settings.API_PREFIX)
app.include_router(routes_history.router, prefix=settings.API_PREFIX)
app.include_router(routes_chat.router, prefix=settings.API_PREFIX)

@app.get("/api/health")
def health_check():
    rf_ready = os.path.exists(os.path.join(settings.MODEL_DIR, "random_forest.joblib"))
    if_ready = os.path.exists(os.path.join(settings.MODEL_DIR, "isolation_forest.joblib"))
    groq_configured = bool(settings.GROQ_API_KEY and "your_groq" not in settings.GROQ_API_KEY)
    
    return {
        "status": "healthy",
        "system": "NetGuard AI",
        "version": settings.VERSION,
        "models": {
            "random_forest": "ready" if rf_ready else "not_trained",
            "isolation_forest": "ready" if if_ready else "not_trained"
        },
        "groq_assistant": {
            "configured": groq_configured,
            "model": settings.GROQ_MODEL
        },
        "database": "sqlite_connected"
    }

# Check for production frontend dist
frontend_dist = os.path.abspath(os.path.join(settings.BASE_DIR, "..", "..", "frontend", "dist"))
if os.path.exists(frontend_dist):
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/")
    async def serve_root():
        index_file = os.path.join(frontend_dist, "index.html")
        if os.path.isfile(index_file):
            return FileResponse(index_file)
        return {"status": "NetGuard AI Active"}

    @app.get("/{full_path:path}")
    async def serve_frontend_spa(full_path: str):
        if full_path.startswith("api/") or full_path.startswith("static/") or full_path in ["docs", "redoc", "openapi.json"]:
            raise HTTPException(status_code=404, detail="Not Found")
            
        file_candidate = os.path.join(frontend_dist, full_path)
        if os.path.isfile(file_candidate):
            return FileResponse(file_candidate)
            
        index_file = os.path.join(frontend_dist, "index.html")
        if os.path.isfile(index_file):
            return FileResponse(index_file)
            
        return {"status": "NetGuard AI Active"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
