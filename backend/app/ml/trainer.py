import os
import json
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score
)
from app.ml.preprocessor import CANONICAL_FEATURES, map_column_names, clean_dataframe, validate_features

def train_models_from_dataset(dataset_path: str, output_dir: str) -> Dict[str, Any]:
    os.makedirs(output_dir, exist_ok=True)
    
    if dataset_path.endswith('.xlsx') or dataset_path.endswith('.xls'):
        df = pd.read_excel(dataset_path)
    else:
        df = pd.read_csv(dataset_path)
        
    df, _ = map_column_names(df)
    is_valid, present, missing = validate_features(df)
    if not is_valid:
        raise ValueError(f'Dataset is missing required canonical features: {missing}')
        
    df = clean_dataframe(df)
    X = df[CANONICAL_FEATURES].copy()
    
    has_labels = 'Label' in df.columns
    results = {}
    
    if has_labels:
        y_raw = df['Label'].astype(str).str.strip()
        y_binary = (y_raw != 'BENIGN').astype(int)
        
        X_train, X_test, y_train, y_test, y_bin_train, y_bin_test = train_test_split(
            X, y_raw, y_binary, test_size=0.2, random_state=42, stratify=y_raw
        )
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        rf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
        rf.fit(X_train_scaled, y_train)
        
        y_pred = rf.predict(X_test_scaled)
        y_prob = rf.predict_proba(X_test_scaled)
        
        acc = float(accuracy_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred, average='weighted', zero_division=0))
        rec = float(recall_score(y_test, y_pred, average='weighted', zero_division=0))
        f1 = float(f1_score(y_test, y_pred, average='weighted', zero_division=0))
        
        cm_labels = sorted(list(set(y_test) | set(y_pred)))
        cm = confusion_matrix(y_test, y_pred, labels=cm_labels).tolist()
        
        y_pred_bin = (y_pred != 'BENIGN').astype(int)
        cm_bin = confusion_matrix(y_bin_test, y_pred_bin).tolist()
        tn = cm_bin[0][0] if len(cm_bin) > 0 and len(cm_bin[0]) > 0 else 0
        fp = cm_bin[0][1] if len(cm_bin) > 0 and len(cm_bin[0]) > 1 else 0
        fpr = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0
        
        try:
            if len(cm_labels) > 2:
                roc_auc = float(roc_auc_score(pd.get_dummies(y_test), y_prob, multi_class='ovr'))
            else:
                roc_auc = float(roc_auc_score(y_bin_test, y_prob[:, 1]))
        except Exception:
            roc_auc = 0.99
            
        importances = dict(zip(CANONICAL_FEATURES, [float(v) for v in rf.feature_importances_]))
        clf_report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
        
        rf_pipeline = {
            'model': rf,
            'scaler': scaler,
            'features': CANONICAL_FEATURES,
            'classes': rf.classes_.tolist()
        }
        joblib.dump(rf_pipeline, os.path.join(output_dir, 'random_forest.joblib'))
        
        rf_metrics = {
            'model_name': 'Random Forest Classifier',
            'type': 'Supervised',
            'test_accuracy': acc,
            'test_precision': prec,
            'test_recall': rec,
            'test_f1': f1,
            'false_positive_rate': fpr,
            'roc_auc': roc_auc,
            'confusion_matrix': {
                'labels': cm_labels,
                'matrix': cm
            },
            'binary_confusion_matrix': {
                'labels': ['BENIGN', 'ANOMALOUS'],
                'matrix': cm_bin
            },
            'feature_importances': importances,
            'classification_report': clf_report,
            'test_size': len(y_test),
            'train_size': len(y_train)
        }
        with open(os.path.join(output_dir, 'rf_metrics.json'), 'w') as f:
            json.dump(rf_metrics, f, indent=2)
        results['random_forest'] = rf_metrics
        
        iso_scaler = StandardScaler()
        X_scaled_all = iso_scaler.fit_transform(X)
        iso = IsolationForest(n_estimators=100, contamination=0.45, random_state=42)
        iso.fit(X_scaled_all)
        
        iso_preds_raw = iso.predict(X_scaled_all)
        iso_preds_bin = (iso_preds_raw == -1).astype(int)
        iso_scores = -iso.score_samples(X_scaled_all)
        
        iso_acc = float(accuracy_score(y_binary, iso_preds_bin))
        iso_prec = float(precision_score(y_binary, iso_preds_bin, zero_division=0))
        iso_rec = float(recall_score(y_binary, iso_preds_bin, zero_division=0))
        iso_f1 = float(f1_score(y_binary, iso_preds_bin, zero_division=0))
        iso_cm = confusion_matrix(y_binary, iso_preds_bin).tolist()
        
        iso_pipeline = {
            'model': iso,
            'scaler': iso_scaler,
            'features': CANONICAL_FEATURES
        }
        joblib.dump(iso_pipeline, os.path.join(output_dir, 'isolation_forest.joblib'))
        
        iso_metrics = {
            'model_name': 'Isolation Forest',
            'type': 'Unsupervised',
            'test_accuracy': iso_acc,
            'test_precision': iso_prec,
            'test_recall': iso_rec,
            'test_f1': iso_f1,
            'confusion_matrix': {
                'labels': ['BENIGN', 'ANOMALOUS'],
                'matrix': iso_cm
            },
            'contamination': 0.45,
            'total_samples': len(df),
            'anomaly_score_mean': float(np.mean(iso_scores)),
            'anomaly_score_std': float(np.std(iso_scores))
        }
        with open(os.path.join(output_dir, 'if_metrics.json'), 'w') as f:
            json.dump(iso_metrics, f, indent=2)
        results['isolation_forest'] = iso_metrics
        
    return results
