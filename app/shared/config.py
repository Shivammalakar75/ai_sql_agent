# app/shared/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    # MySQL
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str
    mysql_database: str = "ai_sql_agent"

    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333

    # Groq  ← gemini ki jagah
    groq_api_key: str

    # App
    app_env: str = "development"
    log_level: str = "INFO"


settings = Settings()