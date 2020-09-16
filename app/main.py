import logging
import sys

import sentry_sdk
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from tortoise.contrib.fastapi import register_tortoise

from app.controllers import tag
from app.core import config

app = FastAPI(
    title="Galaxy",
    servers=[
        {"url": "http://localhost:8000", "description": "Developing environment"},
    ],
    default_response_class=ORJSONResponse,
)
app.include_router(tag.router, tags=["tag"])

logging.root.setLevel("INFO")

if sys.argv[0] != "pytest":  # pragma: no cover
    register_tortoise(
        app,
        config=config.db_config,
        add_exception_handlers=True,
    )
    sentry_sdk.init(dsn=config.settings.sentry_dsn)
    app = SentryAsgiMiddleware(app)
