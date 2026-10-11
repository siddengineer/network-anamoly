import os
import uuid
import json
import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import UploadedDataset
from app.ml.preprocessor import CANONICAL_FEATURES, map_column_names, validate_features
from app.core.config import settings

router = APIRouter(prefix='/datasets', tags=['Datasets'])

@router.post('/preview')
async def preview_dataset(file: UploadFile = File(...)):
    filename = file.filename
    if not (filename.endswith('.csv') or filename.endswith('.xlsx') or filename.endswith('.xls')):
        raise HTTPException(status_code=400, detail='Only .csv, .xlsx, and .xls files are supported.')
        
    try:
        content = await file.read()
        if filename.endswith('.csv'):
            import io
            df = pd.read_csv(io.BytesIO(content))
        else:
            import io
            df = pd.read_excel(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Failed to parse file: {str(e)}')
        
    mapped_df, orig_col_map = map_column_names(df)
    is_valid, present, missing = validate_features(mapped_df)
    
    # preview first 20 records
    preview_df = df.head(20).fillna('')
    preview_records = preview_df.to_dict(orient='records')
    
    return {
        'filename': filename,
        'file_size': len(content),
        'row_count': len(df),
        'column_count': len(df.columns),
        'columns': df.columns.tolist(),
        'canonical_mapped': orig_col_map,
        'is_valid': is_valid,
        'missing_required': missing,
        'preview_records': preview_records
    }

@router.post('/upload')
async def upload_dataset(file: UploadFile = File(...), db: Session = Depends(get_db)):
    filename = file.filename
    if not (filename.endswith('.csv') or filename.endswith('.xlsx') or filename.endswith('.xls')):
        raise HTTPException(status_code=400, detail='Only .csv, .xlsx, and .xls files are supported.')
        
    try:
        content = await file.read()
        if filename.endswith('.csv'):
            import io
            df = pd.read_csv(io.BytesIO(content))
        else:
            import io
            df = pd.read_excel(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Failed to parse file: {str(e)}')
        
    dataset_id = str(uuid.uuid4())
    os.makedirs(settings.DATASETS_DIR, exist_ok=True)
    saved_path = os.path.join(settings.DATASETS_DIR, f'{dataset_id}_{filename}')
    with open(saved_path, 'wb') as f:
        f.write(content)
        
    preview_records = df.head(20).fillna('').to_dict(orient='records')
    
    ds = UploadedDataset(
        id=dataset_id,
        filename=filename,
        file_size=len(content),
        row_count=len(df),
        column_count=len(df.columns),
        columns_json=json.dumps(df.columns.tolist()),
        preview_json=json.dumps(preview_records)
    )
    db.add(ds)
    db.commit()
    db.refresh(ds)
    
    return {
        'id': ds.id,
        'filename': ds.filename,
        'file_size': ds.file_size,
        'row_count': ds.row_count,
        'column_count': ds.column_count,
        'created_at': ds.created_at
    }

@router.get('')
def list_datasets(db: Session = Depends(get_db)):
    datasets = db.query(UploadedDataset).order_by(UploadedDataset.created_at.desc()).all()
    return [
        {
            'id': d.id,
            'filename': d.filename,
            'file_size': d.file_size,
            'row_count': d.row_count,
            'column_count': d.column_count,
            'created_at': d.created_at
        }
        for d in datasets
    ]
