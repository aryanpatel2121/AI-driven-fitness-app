from pydantic_settings import BaseSettings
from typing import List
from pydantic import field_validator

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
    BACKEND_CORS_ORIGINS: List[str] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def cors_preprocess(cls, v):
        """
        Allows both:
        BACKEND_CORS_ORIGINS="https://site1.com,https://site2.com"
        BACKEND_CORS_ORIGINS=["https://site1.com", "https://site2.com"]
        """
        if not v:
            return []
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    # ML Models
    MODEL_PATH: str = "./app/ml/models/"
    
    # AI
    GOOGLE_API_KEY: str | None = None
    CALORIENINJAS_API_KEY: str | None = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
