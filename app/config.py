from pydantic import BaseSettings

from app.utils.paginator import limit_offset_paginator


class Settings(BaseSettings):
    db_url: str = "postgres://postgres:galaxy@localhost:5432/galaxy"


settings = Settings()

DATABASE = {
    "connections": {
        "default": settings.db_url,
    },
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}
pagination = limit_offset_paginator
