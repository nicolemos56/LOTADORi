from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# core -> app -> backend -> raiz do monorepo
ROOT_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(ROOT_DIR / ".env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "TurismoConnect AI Agent"
    database_url: str = (
        "postgresql+psycopg2://turismo:turismo@localhost:5432/turismoconnect"
    )
    cors_origins: str = (
        "http://localhost:5173,http://127.0.0.1:5173,http://[::1]:5173," \
        "http://localhost:5174,http://127.0.0.1:5174,http://[::1]:5174," \
        "http://localhost:4173,http://127.0.0.1:4173,http://[::1]:4173," \
        "http://localhost:3000,http://127.0.0.1:3000,http://[::1]:3000"
    )

    # Chaves LLM (usadas a partir da Sprint 02)
    openai_api_key: str = ""
    groq_api_key: str = ""
    gemini_api_key: str = ""

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
