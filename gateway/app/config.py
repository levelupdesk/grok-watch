from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GROK_WATCH_", env_file=".env", extra="ignore")

    app_name: str = "grok-watch-gateway"
    env: str = "dev"
    jwt_audience: str = "grok-watch"
    jwt_issuer: str = "levelup-worldhub"
    # Dev-only HMAC; production must inject via secret manager.
    jwt_hmac_secret: str = "dev-only-change-me-32b-minimum-secret!!"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/grok_watch"
    audit_enabled: bool = True


settings = Settings()
