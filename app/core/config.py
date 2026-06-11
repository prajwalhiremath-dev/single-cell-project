from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "CellScape"
    environment: str = "local"
    api_v1_prefix: str = "/api/v1"

    database_url: str = "sqlite:///./cellscape.db"
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"

    storage_backend: str = "local"
    local_storage_dir: str = "./data"

    s3_endpoint_url: str | None = None
    s3_access_key_id: str | None = None
    s3_secret_access_key: str | None = None
    s3_bucket_name: str = "cellscape"

    mlflow_tracking_uri: str | None = None
    max_upload_mb: int = Field(default=2048, ge=1)


@lru_cache
def get_settings() -> Settings:
    return Settings()
