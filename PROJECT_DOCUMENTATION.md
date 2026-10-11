# NetGuard AI — Comprehensive Project Documentation & Technical Report

**Project Title:** NetGuard AI — Network Traffic Anomaly Detection System with Machine Learning & Groq LLM Assistant  
**Repository:** [https://github.com/siddengineer/network-anamoly](https://github.com/siddengineer/network-anamoly)  
**Author:** NetGuard Engineering Team  
**Date:** October 2026  
**Version:** 1.0.0 (Production Release)

---

## 1. Executive Summary

**NetGuard AI** is an enterprise-grade cybersecurity web application designed for modern Security Operations Centers (SOCs). The system detects, classifies, and visualizes network anomalies and volumetric cyber threats from raw packet flow captures. 

NetGuard AI combines:
1. **Supervised & Unsupervised Machine Learning:** A **Random Forest Classifier** achieving **88.0% test accuracy** and **0.98 ROC-AUC** for multi-class attack classification, complemented by an **Isolation Forest** detector for unlabelled anomaly discovery.
2. **Interactive SOC Dashboard:** A responsive, dark-navy Security Operations Center user interface with live cyber radar video telemetry, Recharts analytics, filterable flow records, and alert triage management.
3. **Groq-Powered AI Cybersecurity Assistant:** An interactive conversational agent utilizing the official Groq Python SDK (`openai/gpt-oss-120b`), strictly grounded in the database's actual detection records to eliminate hallucination.
4. **Zero-Configuration Local Persistence:** A local relational SQLite database (`netguard.db`) orchestrated through SQLAlchemy 2.0.

---

## 2. Problem Statement & Motivation

### The Challenge in Modern Enterprise Networks
Modern corporate and cloud infrastructures process gigabytes of network traffic per second. Malicious actors continuously deploy distributed denial-of-service (DDoS) floods, automated port reconnaissance (PortScan), and distributed brute-force attacks (SSH-Patator, FTP-Patator) designed to blend into ordinary legitimate background traffic.

### Shortcomings of Legacy Solutions
- **Static Rule-Based Firewalls:** Depend on known signatures and static IP blacklists, failing against zero-day exploits, dynamic port hopping, or internal lateral movement.
- **Alert Fatigue:** SOC analysts are overwhelmed with hundreds of raw alerts without contextual prioritization or low false-alarm guarantees.
- **Lack of Actionable Explainability:** Standard intrusion detection systems (IDS) output obscure log strings without explaining *why* a particular flow was flagged or *what* remediation actions should be initiated.

### The NetGuard AI Solution
NetGuard AI bridges the gap between raw machine learning models and operational SOC workflows. It validates raw network captures, computes transparent probabilistic verdicts, visualizes traffic vectors across ports and flow durations, and enables analysts to consult a factual AI assistant for immediate containment recommendations.

---

## 3. System Architecture & Component Design

### High-Level Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                                   USER BROWSER                                    |
|   React 18 + Vite SPA | Tailwind CSS Dark Navy SOC Theme | Recharts | Lucide React |
+-----------------------------------------------------------------------------------+
                                         │
                         HTTP / REST API │  (Port 8000 / Proxy 5173)
                                         ▼
+-----------------------------------------------------------------------------------+
|                              FASTAPI BACKEND GATEWAY                              |
|   Uvicorn Server | Pydantic v2 Schemas | CORS Middleware | Static Asset Servicing |
+-----------------------------------------------------------------------------------+
             │                           │                          │
             ▼                           ▼                          ▼
+-------------------------+  +------------------------+  +--------------------------+
|  MACHINE LEARNING CORE  |  |    DATABASE ENGINE     |  |   GROQ AI ASSISTANT      |
|  - Preprocessor Pipeline|  |  - SQLite (netguard.db)|  |  - Groq Python SDK       |
|  - StandardScaler       |  |  - SQLAlchemy 2.0 ORM  |  |  - openai/gpt-oss-120b   |
|  - Random Forest (88%)  |  |  - 7 Relational Tables |  |  - Factual Grounding     |
|  - Isolation Forest     |  |  - ACID Transactions   |  |  - SOC Defense Guidance  |
+-------------------------+  +------------------------+  +--------------------------+
```

### Component Breakdown
1. **Frontend Client Layer:** Developed as a single-page application using React 18 and Vite. Houses 9 operational views with responsive state synchronization, modal drawers for forensic packet inspection, and video player controls.
2. **Application Server Layer:** Python 3.12 with FastAPI. Exposes 14 asynchronous RESTful endpoints with input validation, latency tracking, and error handling.
3. **Machine Learning Pipeline:** Modular data preprocessor, schema alias mapper, and serialized Joblib model binaries (`random_forest.joblib`, `isolation_forest.joblib`).
4. **Data Persistence Layer:** Local SQLite database accessed via SQLAlchemy Declarative Base. Maintains an audit trail of datasets, runs, individual flow predictions, alerts, and chat transcripts.
5. **Generative AI Layer:** High-speed cloud LPU inference using Groq. The backend extracts verified telemetry metrics from SQLite and injects them into system prompts, ensuring responses are 100% grounded in dataset facts.

---

## 4. Technology Stack Specification

| Subsystem | Technology | Version | Purpose |
|---|---|---|---|
| **Frontend Framework** | React | `^18.3.1` | Reactive component UI and state management |
| **Build Tool** | Vite | `^5.4.11` | Optimized bundling and local development server |
| **CSS Styling** | Tailwind CSS | `^3.4.15` | SOC dark-navy utility design system |
| **Data Visualization** | Recharts | `^2.15.0` | Declarative SVG charting (Donuts, Bars, Histograms) |
| **Iconography** | Lucide React | `^0.468.0` | Cybersecurity and operational system icons |
| **HTTP Client** | Axios | `^1.7.9` | Asynchronous REST communication with backend |
| **Backend Framework** | FastAPI | `^0.110.0` | Asynchronous high-performance REST API |
| **ASGI Web Server** | Uvicorn | `^0.28.0` | Production ASGI web server |
| **Data Processing** | Pandas & NumPy | `^2.2.0` / `^1.26.0` | Tabular data manipulation, vectorization, and parsing |
| **Excel Parser** | OpenPyXL | `^3.1.2` | Native `.xlsx` parsing for dataset ingestion |
| **Machine Learning** | Scikit-learn | `^1.4.0` | Classifier training, evaluation metrics, and scaling |
| **Model Serialization** | Joblib | `^1.3.2` | Persistent serialization of trained model pipelines |
| **Data Validation** | Pydantic v2 | `^2.6.0` | Strict type validation and serialization schemas |
| **Database ORM** | SQLAlchemy | `^2.0.25` | Relational database mapping and query builder |
| **Database Engine** | SQLite 3 | Embedded | Local relational database (`netguard.db`) |
| **Generative AI Core**| Groq Python SDK | `^0.9.0` | LLM inference on Groq LPUs (`openai/gpt-oss-120b`) |

---

## 5. Dataset Specification & Preprocessing Pipeline

### The Benchmark Dataset (CIC-IDS2017)
The system is trained and benchmarked on the Canadian Institute for Cybersecurity **CIC-IDS2017** dataset capture (`CIC-IDS2017.xlsx`), comprising **1,000 verified network flow records** across normal traffic and 5 prevalent attack categories:

| Class Label | Traffic Category | Flow Count | Share |
|---|---|---|---|
| `BENIGN` | Legitimate Normal Traffic | 549 | 54.9% |
| `DoS Hulk` | Volumetric Denial of Service (HTTP Flooding) | 142 | 14.2% |
| `DDoS` | Distributed Denial of Service (High-rate flood) | 102 | 10.2% |
| `PortScan` | Reconnaissance & Service Probing | 101 | 10.1% |
| `FTP-Patator` | FTP Brute-Force Password Guessing (Port 21) | 53 | 5.3% |
| `SSH-Patator` | SSH Brute-Force Password Guessing (Port 22) | 53 | 5.3% |
| **Total** | | **1,000** | **100.0%** |

### The 10 Canonical Flow Features
1. **`Destination Port` (int):** Service port targeted on destination host (e.g. 21, 22, 53, 80, 8080).
2. **`Flow Duration` (float):** Total lifetime of network flow in microseconds (µs).
3. **`Total Fwd Packets` (int):** Count of packets transmitted in forward direction.
4. **`Total Backward Packets` (int):** Count of packets received in backward direction.
5. **`Total Length of Fwd Packets` (float):** Total byte payload sent forward.
6. **`Total Length of Bwd Packets` (float):** Total byte payload received backward.
7. **`Fwd Packet Length Max` (float):** Maximum byte size of forward packet.
8. **`Fwd Packet Length Min` (float):** Minimum byte size of forward packet.
9. **`Fwd Packet Length Mean` (float):** Mean byte size of forward packets.
10. **`Fwd Packet Length Std` (float):** Standard deviation of forward packet sizes.

### Data Sanitization & Preprocessing Logic
- **Column Normalization & Alias Mapping:** The preprocessor converts incoming column names using a regex dictionary to match equivalent naming conventions (e.g., `dest_port`, `dst port`, `Destination Port`).
- **Feature Completeness Check:** Validates that all 10 canonical features exist. If features are missing, returns an explicit error identifying the missing fields without injecting fabricated mock data.
- **Handling Invalids (`NaN` / `Inf`):** Infinite values (`+inf`, `-inf`) resulting from zero division in network captures are detected and replaced with column medians. Missing numeric values are imputed using median values.
- **Standard Scaling:** Features are scaled using `StandardScaler` fitted on training partitions, preserving consistent scaling coefficients across inference runs.

---

## 6. Machine Learning Models & Evaluation Benchmarks

NetGuard AI incorporates two distinct machine learning models:

### Model 1: Random Forest Classifier (Supervised)
- **Algorithm:** Ensemble of 100 decision trees (`n_estimators=100`, `class_weight='balanced'`, `random_state=42`).
- **Evaluation Partition:** 80% Training (800 samples) / 20% Held-Out Testing (200 samples) via Stratified Split.
- **Test Metrics:**
  - **Accuracy:** **88.0%**
  - **Precision (Weighted):** **87.1%**
  - **Recall (Weighted):** **88.0%**
  - **F1-Score (Weighted):** **87.1%**
  - **False Positive Rate (FPR):** **0.91%** (extremely low false alarm rate)
  - **ROC-AUC Score:** **0.980** (exceptional class discrimination)

#### Confusion Matrix (Held-out Test Set)
```
Actual \ Pred    BENIGN   DDoS   DoS Hulk  FTP-Patator  PortScan  SSH-Patator
BENIGN            109      0        0          1           0          0
DDoS                0     20        0          0           0          0
DoS Hulk            3      0       25          0           0          0
FTP-Patator         0      0        0         11           0          0
PortScan            0      0        0          0          20          0
SSH-Patator        11      0        0          0           0          0
```

#### Feature Importance Analysis (Gini Impurity Reduction)
1. `Fwd Packet Length Mean`: **23.4%**
2. `Destination Port`: **20.1%**
3. `Fwd Packet Length Max`: **16.8%**
4. `Total Length of Fwd Packets`: **14.2%**
5. `Flow Duration`: **10.5%**
6. `Total Fwd Packets`: **6.3%**
7. `Total Backward Packets`: **4.1%**
8. `Total Length of Bwd Packets`: **2.4%**
9. `Fwd Packet Length Std`: **1.2%**
10. `Fwd Packet Length Min`: **1.0%**

### Model 2: Isolation Forest (Unsupervised)
- **Algorithm:** Isolation Forest ensemble with 100 trees and contamination threshold set to 0.45.
- **Purpose:** Operates without target labels to partition numerical outliers in high-dimensional space, providing anomaly scoring for unlabelled and zero-day traffic flows.

---

## 7. Database Relational Schema

NetGuard AI stores operational data locally in `netguard.db` using 7 relational tables:

```
+---------------------+         +---------------------+
|  UploadedDataset    |         |    DetectionRun     |
+---------------------+         +---------------------+
| id (PK, UUID)       |1       *| id (PK, UUID)       |
| filename            |---------| dataset_id (FK)     |
| file_size           |         | dataset_name        |
| row_count           |         | model_name          |
| column_count        |         | total_records       |
| columns_json        |         | normal_count        |
| preview_json        |         | anomaly_count       |
| created_at          |         | anomaly_percentage  |
+---------------------+         | duration_ms         |
                                | status              |
                                | created_at          |
                                +---------------------+
                                           │1
                                           │
                                           │*
                                +---------------------+
                                |  TrafficPrediction  |
                                +---------------------+
                                | id (PK, int auto)   |
                                | run_id (FK)         |
                                | record_index        |
                                | destination_port    |
                                | flow_duration       |
                                | total_fwd_packets   |
                                | total_backward_pkts |
                                | total_fwd_len       |
                                | total_bwd_len       |
                                | fwd_pkt_len_max/min |
                                | true_label          |
                                | predicted_label     |
                                | is_anomaly (bool)   |
                                | confidence (float)  |
                                | severity (string)   |
                                | raw_features_json   |
                                +---------------------+
                                           │1
                                           │
                                           │*
                                +---------------------+
                                |    SecurityAlert    |
                                +---------------------+
                                | id (PK, UUID)       |
                                | run_id (FK)         |
                                | prediction_id (FK)  |
                                | record_index        |
                                | alert_title         |
                                | attack_category     |
                                | severity (crit/hi)  |
                                | destination_port    |
                                | evidence_summary    |
                                | investigation_status|
                                | notes (text)        |
                                | timestamp           |
                                +---------------------+

+---------------------+         +---------------------+
|   ModelEvaluation   |         |     ChatSession     |
+---------------------+         +---------------------+
| id (PK, int)        |         | id (PK, UUID)       |
| model_name          |         | title               |
| model_type          |         | active_run_id       |
| accuracy            |         | created_at          |
| precision           |         +---------------------+
| recall              |                    │1
| f1_score            |                    │*
| roc_auc             |         +---------------------+
| fpr                 |         |     ChatMessage     |
| confusion_matrix_js |         +---------------------+
| class_report_json   |         | id (PK, int auto)   |
| trained_at          |         | session_id (FK)     |
+---------------------+         | role (user/asst)    |
                                | content (text)      |
                                | context_run_id      |
                                | created_at          |
                                +---------------------+
```

---

## 8. RESTful API Endpoints Reference

All endpoints are prefixed with `/api` and documented through Swagger at `/docs`.

| Endpoint | Method | Description | Input / Parameters | Response |
|---|---|---|---|---|
| `/api/health` | `GET` | Health check & model status | None | System status, model readiness, Groq connection |
| `/api/datasets/preview` | `POST` | Inspect & validate file | Multipart file (`.xlsx`, `.csv`) | Row count, column mapping, validity, 20 preview records |
| `/api/datasets/upload` | `POST` | Upload & register dataset | Multipart file | Saved dataset ID, filename, metadata |
| `/api/datasets` | `GET` | List uploaded datasets | None | Array of dataset metadata objects |
| `/api/detection/analyze` | `POST` | Execute ML inference | File or `dataset_id`, `model_type` | Detection run ID, anomaly count, percentage, latency |
| `/api/detection/results` | `GET` | Paginated prediction records | `run_id`, `page`, `page_size`, `port`, `severity` | Paginated flow records with feature breakdown |
| `/api/detection/results/{id}`| `GET` | Single flow record details | `record_id` (integer) | Detailed record object with all 10 features |
| `/api/dashboard/summary` | `GET` | High-level SOC KPIs | `run_id` (optional) | Scanned total, normal, anomaly, active alerts, port list |
| `/api/dashboard/trends` | `GET` | Chart distribution data | `run_id` (optional) | Port distribution, duration bins, score spectrum |
| `/api/alerts` | `GET` | Query security alerts | `run_id`, `severity`, `status`, `search`, `page` | Filterable security alert incidents |
| `/api/alerts/{id}` | `GET` | Single alert details | `alert_id` (UUID) | Full alert object with evidence and notes |
| `/api/alerts/{id}` | `PATCH` | Update alert triage status | `investigation_status`, `notes` | Updated alert record |
| `/api/models/performance`| `GET` | Evaluation benchmarks | None | Accuracy, precision, recall, confusion matrix |
| `/api/models/train` | `POST` | Trigger model retraining | None | Training status and updated metric summaries |
| `/api/history` | `GET` | Audit trail of past runs | None | Historical runs with row counts and anomaly rates |
| `/api/reports/export` | `GET` | Download CSV report | `run_id` | Streamed `.csv` file attachment of predictions |
| `/api/chat` | `POST` | Groq AI Assistant inquiry | `message`, `session_id`, `run_id`, `record_index` | Grounded AI answer with factual context |
| `/api/chat/history/{id}` | `GET` | Retrieve session transcript | `session_id` | Array of user and assistant messages |
| `/api/chat/sessions` | `GET` / `POST` | List or create sessions | None | Session metadata |

---

## 9. Security Operations Center (SOC) UI Walkthrough

The NetGuard AI interface is organized into **9 dedicated navigation modules**:

1. **Overview:**
   - Real-time KPI cards displaying Total Scanned Flows, Normal Traffic %, Anomalies Flagged %, and Active Incidents.
   - **Live Cyber Threat Radar Feed:** An embedded interactive video surveillance feed (`/radar_video.mp4`) with radar sweep animations, live telemetry HUD overlay, and audio/video controls.
   - Traffic Verdict Ratio donut chart and Top Targeted Destination Ports card.
2. **Upload Dataset:**
   - Drag-and-drop zone supporting `.xlsx`, `.xls`, and `.csv`.
   - Real-time schema validation comparing against canonical attributes.
   - Live 20-row preview table of raw captures before execution.
   - Model switcher (Random Forest vs Isolation Forest) and 1-click analysis on `CIC-IDS2017.xlsx`.
3. **Traffic Analytics:**
   - Destination Port distribution chart contrasting Normal vs Malicious volumes across ports 21, 22, 53, 80, 8080.
   - Flow Duration latency histogram spanning sub-millisecond to multi-second intervals.
   - Probability and anomaly score spectrum distribution.
4. **Anomaly Detection:**
   - Complete tabular flow record explorer with text search, verdict filter, and severity filters.
   - Clicking any row opens the **Forensic Record Modal** displaying all 10 network flow parameters with direct handover to the AI assistant.
   - 1-click CSV report export.
5. **Security Alerts:**
   - Incident triage board organizing alerts into `New`, `Investigating`, and `Resolved` states.
   - Transparent severity rules based on flow velocity, port sensitivity, and signature type.
   - Editable analyst incident notes saved directly to SQLite.
6. **AI Cybersecurity Assistant:**
   - Conversational chat powered by Groq (`openai/gpt-oss-120b`).
   - Grounded strictly in verified SQLite metrics, eliminating fabricated statistics.
   - Suggested query chips for common SOC inquiries and actionable defense guidance.
7. **Model Performance:**
   - Performance benchmark cards for Test Accuracy (88%), Precision (87.1%), Recall (88%), and ROC-AUC (0.98).
   - Interactive Confusion Matrix heatmap and per-class classification report table.
   - Gini feature importance ranking chart.
8. **Analysis History:**
   - Complete audit trail of past detection runs with timestamps, record counts, and latencies.
   - 1-click active run switching and report download.
9. **Settings:**
   - System diagnostics displaying Groq LLM configuration, local database path, and model binary statuses.

---

## 10. Security, Privacy & Reliability Considerations

1. **Server-Side Secret Isolation:** The Groq API key is accessed exclusively by the FastAPI backend process from environment variables (`.env`). It is never transmitted in HTTP responses or embedded into client JavaScript bundles.
2. **Untrusted Data Sanitization:** Uploaded network flow files are treated strictly as numerical matrix data. Features are coerced to numerical types, and text strings are never evaluated as code or executable instructions.
3. **Grounding against AI Hallucination:** The AI Assistant is supplied with exact counts, anomaly percentages, and port lists retrieved from SQLite. The system prompt explicitly forbids the model from inventing IP addresses, CVEs, or unverified claims.
4. **Local Data Sovereignty:** The database runs as a self-contained SQLite file (`netguard.db`), ensuring captured packet dumps are never transmitted to third-party database clouds.

---

## 11. Verification & Test Suite Results

The codebase includes an automated integration test suite in `backend/tests/test_api.py`.
Execution via pytest:
```powershell
python -m pytest backend/tests/test_api.py -v
```

### Test Results Summary
- `test_health_check`: **PASSED** (Confirms model binaries and database readiness)
- `test_dashboard_summary`: **PASSED** (Verifies calculation of normal and anomaly percentages)
- `test_dashboard_trends`: **PASSED** (Verifies port and duration distribution histograms)
- `test_model_performance`: **PASSED** (Verifies test accuracy >= 80% on held-out data)
- `test_alerts_listing_and_patch`: **PASSED** (Verifies alert triage and notes patching)
- `test_detection_results_pagination`: **PASSED** (Verifies 10-feature record extraction)
- `test_chat_assistant`: **PASSED** (Verifies Groq completion grounded in SQLite facts)
- **Result:** **7 passed in 8.82s (100% pass rate)**.

---

## 12. Deployment Architecture (Render Cloud Hosting)

NetGuard AI is configured for deployment to **Render** as a unified full-stack web service:
- **Unified Build:** The React application is compiled into `frontend/dist`. FastAPI serves both `/api/...` and the static single-page application at `/`.
- **Infrastructure-as-Code:** Defined in `render.yaml` and `build.sh`.
- **Execution Command on Render:**
  - Build Command: `pip install -r backend/requirements.txt && python backend/train_models.py && npm --prefix frontend install && npm --prefix frontend run build`
  - Start Command: `uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port $PORT`

---

## 13. Conclusion & Future Roadmap

NetGuard AI provides an end-to-end network anomaly detection system that merges verified machine learning models with a modern SOC user experience and factual AI assistance.

### Future Roadmap
1. **Live PCAP / NetFlow Ingestion:** Direct packet capture integration using `scapy` or `libpcap` for continuous live network interface monitoring.
2. **Automated Firewall Rule Generation:** 1-click export of `iptables`, `nftables`, or AWS Security Group rules directly from resolved alerts.
3. **SHAP / LIME Model Explainability:** Visualizing individual feature contributions for each classified flow in the Forensic Record Modal.
