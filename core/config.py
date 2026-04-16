from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AI-Agent-Challenge"
    APP_VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"
    LOG_LEVEL: str = "INFO"
    
    MODEL_PATH_ISOLATION_FOREST: str = "models/saved/isolation_forest.pkl"
    MODEL_PATH_XGBOOST: str = "models/saved/xgboost.pkl"

    class Config:
        env_file = ".env"

settings = Settings()