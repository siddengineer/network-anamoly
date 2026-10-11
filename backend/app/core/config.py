import os
from typing import List
from dotenv import load_dotenv

# Load backend/.env if present
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

class Settings:
    PROJECT_NAME: str = 'NetGuard AI'
    VERSION: str = '1.0.0'
    API_PREFIX: str = '/api'
    
    GROQ_API_KEY: str = os.getenv('GROQ_API_KEY', '')
    GROQ_MODEL: str = os.getenv('GROQ_MODEL', 'openai/gpt-oss-120b')
    
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///./netguard.db')
    
    CORS_ORIGINS: List[str] = [
        o.strip() for o in os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000').split(',') if o.strip()
    ]
    
    HOST: str = os.getenv('HOST', '127.0.0.1')
    PORT: int = int(os.getenv('PORT', '8000'))
    
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_DIR: str = os.path.join(BASE_DIR, 'ml', 'saved_models')
    STATIC_DIR: str = os.path.join(BASE_DIR, 'static')
    DATASETS_DIR: str = os.path.join(os.path.dirname(BASE_DIR), 'datasets')

settings = Settings()
