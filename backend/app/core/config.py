from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Fitness Tracker API"
    
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # ML Models
    MODEL_PATH: str = "./app/ml/models/"
    
    # AI
    GOOGLE_API_KEY: str | None = None
    CALORIENINJAS_API_KEY: str | None = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
