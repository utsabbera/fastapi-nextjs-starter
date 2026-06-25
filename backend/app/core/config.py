from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "FastAPI App"
    database_url: str = "postgresql+asyncpg://dev:dev@localhost:5432/app_dev"
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 30
    cors_origins: list[str] = ["http://localhost:3000"]

    @property
    def is_production(self) -> bool:
        return "localhost" not in self.database_url


settings = Settings()
