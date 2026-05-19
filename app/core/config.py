
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

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

    schema_collection_name: str = "nl_sql_schema"
    embedding_dim: int = 384
    top_k_schemas: int = 3
    embedding_model: str = "all-MiniLM-L6-v2"

    # Groq / LLM
    groq_api_key: str

    llm_model: str = "llama-3.3-70b-versatile"
    llm_max_tokens: int = 1024
    llm_temperature: float = 0.0

    # SQL Safety
    sql_allowed_statements: list[str] = Field(default_factory=lambda: ["SELECT"])
    sql_max_rows: int = 100

    # Tables
    db_tables: list[str] = Field(
        default_factory=lambda: ["users", "orders", "products"]
    )

    # App
    app_env: str = "development"
    log_level: str = "INFO"


settings = Settings()