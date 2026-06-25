from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Finance Discipline"
    database_url: str = "postgresql+asyncpg://finance:finance@db:5432/finance"
    database_url_sync: str = "postgresql+psycopg2://finance:finance@db:5432/finance"
    secret_key: str = "super-secret-key-change-in-production"
    openai_api_key: str = ""
    telegram_bot_token: str = ""
    debug: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
