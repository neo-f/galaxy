from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app import config

app = FastAPI(
    title="Tortoise ORM FastAPI example",
    servers=[
        {"url": "http://localhost:8000", "description": "Staging environment"},
    ],
)


register_tortoise(
    app,
    config=config.DATABASE,
    generate_schemas=True,
    add_exception_handlers=True,
)
