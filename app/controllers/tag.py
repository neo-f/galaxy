from typing import List

from fastapi import Depends
from tortoise.contrib.fastapi import HTTPNotFoundError

from app import config
from app.controllers import Status
from app.models import Tag, TagDetail, TagCreate
from app.server import app


@app.get("/tag", response_model=List[TagDetail])
async def list_tags(paginator=Depends(config.pagination)):
    qs = Tag.all().limit(paginator.limit).offset(paginator.offset)
    return await TagDetail.from_queryset(qs)


@app.post("/tag", response_model=TagDetail)
async def create_tag(tag: TagCreate):
    tag = await Tag.create(**tag.dict(exclude_unset=True))
    return await TagDetail.from_tortoise_orm(tag)


@app.put("/tag/{tag_id}", response_model=TagDetail, responses={404: {"model": HTTPNotFoundError}})
async def update_tag(tag_id: int, tag: TagCreate):
    obj = await Tag.get(pk=tag_id)
    obj = obj.update_from_dict(tag.dict(exclude_unset=True))
    await obj.save()
    return await TagDetail.from_tortoise_orm(obj)


@app.get("/tag/{tag_id}", response_model=TagDetail, responses={404: {"model": HTTPNotFoundError}})
async def get_tag(tag_id: int):
    obj = await Tag.get(pk=tag_id)
    return await TagDetail.from_tortoise_orm(obj)


@app.delete("/tag/{tag_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_tag(tag_id: int):
    obj = await Tag.get(pk=tag_id)
    await obj.delete()
    return Status(message=f"Deleted tag {tag_id}")
