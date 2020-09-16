from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn
from tortoise import generate_config


class Settings(BaseSettings):
    mode: str = "dev"
    postgres_dsn: PostgresDsn = "postgres://postgres:galaxy@localhost:5432/galaxy"
    postgres_dsn_test: PostgresDsn = "postgres://postgres:galaxy@localhost:5432/galaxy_{}"
    sentry_dsn: AnyHttpUrl = "https://4191639452fc45deb6259e1d1992a9a4@o418626.ingest.sentry.io/5423877"


settings = Settings()

db_config = generate_config(db_url=settings.postgres_dsn, app_modules={"models": ["app.models", "aerich.models"]})
