import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
from app.ml.preprocessor import CANONICAL_FEATURES, map_column_names, clean_dataframe, validate_features

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'saved_models')

_models_cache = {}

def get_model_pipeline(model_type: str = 'random_forest'):
    if model_type in _models_cache:
        return _models_cache[model_type]
        
    filename = 'random_forest.joblib' if model_type == 'random_forest' else 'isolation_forest.joblib'
    filepath = os.path.join(MODEL_DIR, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'Trained model file not found at {filepath}. Please train the model first.')
        
    pipeline = joblib.load(filepath)
    _models_cache[model_type] = pipeline
    return pipeline

def assign_severity(pred_label: str, dest_port: int, flow_duration: float, total_pkts: float, score: float) -> str:
    norm_label = pred_label.upper()
    if 'DDOS' in norm_label or 'DOS' in norm_label:
        if total_pkts > 50 or flow_duration > 1000000 or dest_port in [80, 443, 8080]:
            return 'critical'
        return 'high'
    elif 'PATATOR' in norm_label or 'SSH' in norm_label or 'FTP' in norm_label or dest_port in [21, 22]:
        return 'high'
    elif 'PORTSCAN' in norm_label or 'SCAN' in norm_label:
        return 'high' if dest_port < 1024 else 'medium'
    elif norm_label in ['ANOMALOUS', 'ANOMALY']:
        if score > 0.7:
            return 'critical'
        elif score > 0.55:
            return 'high'
        elif score > 0.45:
            return 'medium'
        return 'low'
    return 'low'

def predict_dataframe(df: pd.DataFrame, model_type: str = 'random_forest') -> Dict[str, Any]:
    mapped_df, orig_col_map = map_column_names(df)
    is_valid, present, missing = validate_features(mapped_df)
    if not is_valid:
        raise ValueError(f'Uploaded dataset is missing required features: {missing}')
        
    cleaned_df = clean_dataframe(mapped_df)
    X = cleaned_df[CANONICAL_FEATURES].copy()
    
    pipeline = get_model_pipeline(model_type)
    scaler = pipeline['scaler']
    model = pipeline['model']
    
    X_scaled = scaler.transform(X)
    
    records = []
    normal_count = 0
    anomaly_count = 0
    
    has_labels = 'Label' in mapped_df.columns
    
    if model_type == 'random_forest':
        preds = model.predict(X_scaled)
        probs = model.predict_proba(X_scaled)
        classes = model.classes_
        
        for idx in range(len(df)):
            pred_cls = str(preds[idx])
            pred_probs = probs[idx]
            conf = float(np.max(pred_probs))
            is_anomaly = (pred_cls != 'BENIGN')
            
            if is_anomaly:
                anomaly_count += 1
            else:
                normal_count += 1
                
            port = int(cleaned_df.iloc[idx]['Destination Port'])
            dur = float(cleaned_df.iloc[idx]['Flow Duration'])
            fwd_p = float(cleaned_df.iloc[idx]['Total Fwd Packets'])
            bwd_p = float(cleaned_df.iloc[idx]['Total Backward Packets'])
            tot_p = fwd_p + bwd_p
            
            severity = assign_severity(pred_cls, port, dur, tot_p, conf) if is_anomaly else 'low'
            true_lbl = str(mapped_df.iloc[idx]['Label']) if has_labels else None
            
            raw_feats = {col: float(cleaned_df.iloc[idx][col]) for col in CANONICAL_FEATURES}
            
            records.append({
                'record_index': idx,
                'destination_port': port,
                'flow_duration': dur,
                'total_fwd_packets': int(fwd_p),
                'total_backward_packets': int(bwd_p),
                'total_fwd_len': float(cleaned_df.iloc[idx]['Total Length of Fwd Packets']),
                'total_bwd_len': float(cleaned_df.iloc[idx]['Total Length of Bwd Packets']),
                'fwd_pkt_len_max': float(cleaned_df.iloc[idx]['Fwd Packet Length Max']),
                'fwd_pkt_len_min': float(cleaned_df.iloc[idx]['Fwd Packet Length Min']),
                'fwd_pkt_len_mean': float(cleaned_df.iloc[idx]['Fwd Packet Length Mean']),
                'fwd_pkt_len_std': float(cleaned_df.iloc[idx]['Fwd Packet Length Std']),
                'true_label': true_lbl,
                'predicted_label': pred_cls,
                'is_anomaly': is_anomaly,
                'anomaly_score': conf,
                'confidence': conf,
                'severity': severity,
                'raw_features': raw_feats
            })
    else:
        # Isolation Forest
        raw_preds = model.predict(X_scaled)
        raw_scores = -model.score_samples(X_scaled)
        
        # normalize score roughly to [0, 1]
        min_s = float(np.min(raw_scores))
        max_s = float(np.max(raw_scores))
        rng = (max_s - min_s) if (max_s - min_s) > 0 else 1.0
        norm_scores = (raw_scores - min_s) / rng
        
        for idx in range(len(df)):
            is_anomaly = bool(raw_preds[idx] == -1)
            pred_cls = 'ANOMALOUS' if is_anomaly else 'BENIGN'
            score = float(norm_scores[idx])
            
            if is_anomaly:
                anomaly_count += 1
            else:
                normal_count += 1
                
            port = int(cleaned_df.iloc[idx]['Destination Port'])
            dur = float(cleaned_df.iloc[idx]['Flow Duration'])
            fwd_p = float(cleaned_df.iloc[idx]['Total Fwd Packets'])
            bwd_p = float(cleaned_df.iloc[idx]['Total Backward Packets'])
            tot_p = fwd_p + bwd_p
            
            severity = assign_severity('ANOMALOUS', port, dur, tot_p, score) if is_anomaly else 'low'
            true_lbl = str(mapped_df.iloc[idx]['Label']) if has_labels else None
            raw_feats = {col: float(cleaned_df.iloc[idx][col]) for col in CANONICAL_FEATURES}
            
            records.append({
                'record_index': idx,
                'destination_port': port,
                'flow_duration': dur,
                'total_fwd_packets': int(fwd_p),
                'total_backward_packets': int(bwd_p),
                'total_fwd_len': float(cleaned_df.iloc[idx]['Total Length of Fwd Packets']),
                'total_bwd_len': float(cleaned_df.iloc[idx]['Total Length of Bwd Packets']),
                'fwd_pkt_len_max': float(cleaned_df.iloc[idx]['Fwd Packet Length Max']),
                'fwd_pkt_len_min': float(cleaned_df.iloc[idx]['Fwd Packet Length Min']),
                'fwd_pkt_len_mean': float(cleaned_df.iloc[idx]['Fwd Packet Length Mean']),
                'fwd_pkt_len_std': float(cleaned_df.iloc[idx]['Fwd Packet Length Std']),
                'true_label': true_lbl,
                'predicted_label': pred_cls,
                'is_anomaly': is_anomaly,
                'anomaly_score': score,
                'confidence': score,
                'severity': severity,
                'raw_features': raw_feats
            })
            
    total = len(df)
    anomaly_pct = round((anomaly_count / total * 100.0), 2) if total > 0 else 0.0
    
    return {
        'total_records': total,
        'normal_count': normal_count,
        'anomaly_count': anomaly_count,
        'anomaly_percentage': anomaly_pct,
        'records': records
    }
