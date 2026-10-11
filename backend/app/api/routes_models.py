import os
import json
from fastapi import APIRouter, HTTPException
from app.core.config import settings
from app.ml.trainer import train_models_from_dataset

router = APIRouter(prefix='/models', tags=['Models'])

@router.get('/performance')
def get_model_performance():
    rf_path = os.path.join(settings.MODEL_DIR, 'rf_metrics.json')
    if_path = os.path.join(settings.MODEL_DIR, 'if_metrics.json')
    
    rf_data = None
    if_data = None
    
    if os.path.exists(rf_path):
        with open(rf_path, 'r') as f:
            rf_data = json.load(f)
            
    if os.path.exists(if_path):
        with open(if_path, 'r') as f:
            if_data = json.load(f)
            
    if not rf_data and not if_data:
        raise HTTPException(
            status_code=404,
            detail='Model evaluation metrics not found. Please train models first using the train endpoint.'
        )
        
    return {
        'random_forest': rf_data,
        'isolation_forest': if_data
    }

@router.post('/train')
def trigger_train_models():
    dataset_path = os.path.join(os.path.dirname(settings.DATASETS_DIR), 'CIC-IDS2017.xlsx')
    if not os.path.exists(dataset_path):
        dataset_path = os.path.join(settings.DATASETS_DIR, 'CIC-IDS2017.xlsx')
    if not os.path.exists(dataset_path):
        raise HTTPException(status_code=404, detail='Dataset CIC-IDS2017.xlsx not found to train models.')
        
    try:
        results = train_models_from_dataset(dataset_path, settings.MODEL_DIR)
        return {'status': 'success', 'message': 'Models retrained successfully', 'results': results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Training failed: {str(e)}')
