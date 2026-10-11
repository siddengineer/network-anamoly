import sys
import os

# Ensure backend root is in python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from app.ml.trainer import train_models_from_dataset

def main():
    dataset_path = os.path.join(backend_dir, '..', 'CIC-IDS2017.xlsx')
    if not os.path.exists(dataset_path):
        dataset_path = os.path.join(backend_dir, '..', 'datasets', 'CIC-IDS2017.xlsx')
        
    print(f'Training models using dataset: {dataset_path}')
    output_dir = os.path.join(backend_dir, 'app', 'ml', 'saved_models')
    
    results = train_models_from_dataset(dataset_path, output_dir)
    print('Training complete!')
    print('Random Forest Test Metrics:', {
        k: v for k, v in results['random_forest'].items() if k in ['test_accuracy', 'test_precision', 'test_recall', 'test_f1', 'false_positive_rate', 'roc_auc']
    })
    print('Isolation Forest Metrics:', {
        k: v for k, v in results['isolation_forest'].items() if k in ['test_accuracy', 'test_precision', 'test_recall', 'test_f1']
    })

if __name__ == '__main__':
    main()
