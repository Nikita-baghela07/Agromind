from pydantic import BaseSettings, AnyHttpUrl, Field
from typing import Optional


class Settings(BaseSettings):
    # Basic
    PROJECT_NAME: str = "AgroMind"
    ENV: str = "development"
    DEBUG: bool = True

    # App
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    FASTAPI_URL: Optional[AnyHttpUrl] = None

    # Database
    DATABASE_URL: str = "sqlite:///./agromind.db"  # swap to postgres in prod

    # Models
    MODEL_PATH: str = "app/ml/Dieases_model.pkl"
    CROP_MODEL_PATH: str = "app/ml/crop_model.pkl"

    # Security / JWT
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # Cloud / Integrations
    OPENWEATHER_API_KEY: Optional[str] = None
    SOIL_API_KEY: Optional[str] = None
    MARKET_API_KEY: Optional[str] = None

    # S3 / Storage
    S3_ENDPOINT: Optional[str] = None
    S3_BUCKET: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    S3_REGION: Optional[str] = None

    # MQTT / IoT
    MQTT_HOST: str = "localhost"
    MQTT_PORT: int = 1883
    MQTT_USER: Optional[str] = None
    MQTT_PASS: Optional[str] = None
    MQTT_TOPIC_PREFIX: str = "agromind/"

    # Celery / Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: Optional[str] = None  # e.g. redis://...
    CELERY_BACKEND_URL: Optional[str] = None

    # Vector DB
    VECTOR_DB_URL: Optional[str] = None

    # Misc
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# instantiate global settings object
settings = Settings()
