from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "FastAPI App"
    debug: bool = True
    database_url: str = "postgresql+asyncpg://dev:dev@localhost:5432/app_dev"
    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
