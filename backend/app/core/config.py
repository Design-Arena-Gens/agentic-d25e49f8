from pydantic_settings import BaseSettings
from pydantic import AnyUrl
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "PerplexiPlay API"
    api_v1_prefix: str = "/api"

    secret_key: str = "changeme"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    jwt_algorithm: str = "HS256"

    database_url: str = "sqlite:///./perplexiplay.db"

    # CORS
    backend_cors_origins: str = "*"

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
