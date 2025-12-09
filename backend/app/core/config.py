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

    # CORS - Make it optional with a sensible default
    BACKEND_CORS_ORIGINS: List[str] | str = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def cors_preprocess(cls, v):
        """
        Allows both:
        BACKEND_CORS_ORIGINS="https://site1.com,https://site2.com"
        BACKEND_CORS_ORIGINS=["https://site1.com", "https://site2.com"]
        
        Also handles None and empty string gracefully.
        """
        # Handle None or empty string
        if not v or (isinstance(v, str) and not v.strip()):
            return []
        
        # Already a list/tuple - return as is
        if isinstance(v, (list, tuple)):
            return [str(i) for i in v]
        
        # Handle string input
        if isinstance(v, str):
            v = v.strip()
            
            # Try JSON parsing first (for ["url1","url2"] format)
            if v.startswith('[') and v.endswith(']'):
                try:
                    import json
                    parsed = json.loads(v)
                    if isinstance(parsed, (list, tuple)):
                        return [str(i) for i in parsed]
                except Exception:
                    pass  # Fall through to comma-separated parsing
            
            # Fallback to comma-separated
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        
        return []

    # ML Models
    MODEL_PATH: str = "./app/ml/models/"
    
    # AI
    GOOGLE_API_KEY: str | None = None
    CALORIENINJAS_API_KEY: str | None = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
