from fastapi import APIRouter, Depends
from tortoise.contrib.fastapi import HTTPNotFoundError

from app.controllers import Status
from app.models import Tag, TagCreate, TagDetail
from app.utils.paginator import Pagination, PaginationResult

router = APIRouter()


@router.get("/tag", response_model=PaginationResult[TagDetail])
async def list_tags(paginator=Depends(Pagination)):
    qs = Tag.all()
    return await paginator.paginate(qs)


@router.post("/tag", response_model=TagDetail)
async def create_tag(tag: TagCreate):
    tag = await Tag.create(**tag.dict(exclude_unset=True))
    return await TagDetail.from_tortoise_orm(tag)


@router.put("/tag/{tag_id}", response_model=TagDetail, responses={404: {"model": HTTPNotFoundError}})
async def update_tag(tag_id: int, tag: TagCreate):
    obj = await Tag.get(pk=tag_id)
    obj = obj.update_from_dict(tag.dict(exclude_unset=True))
    await obj.save()
    return await TagDetail.from_tortoise_orm(obj)


@router.get("/tag/{tag_id}", response_model=TagDetail, responses={404: {"model": HTTPNotFoundError}})
async def get_tag(tag_id: int):
    obj = await Tag.get(pk=tag_id)
    return await TagDetail.from_tortoise_orm(obj)


@router.delete("/tag/{tag_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_tag(tag_id: int):
    obj = await Tag.get(pk=tag_id)
    await obj.delete()
    return Status(message=f"Deleted tag {tag_id}")
