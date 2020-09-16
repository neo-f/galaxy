import asyncio
from typing import Generic, List, TypeVar

from fastapi import HTTPException, Query
from pydantic.generics import GenericModel
from tortoise import QuerySet
from tortoise.exceptions import FieldError

default_offset = 0
max_offset = None

default_limit = 10
max_limit = 1000

DataT = TypeVar("DataT")


class PaginationResult(GenericModel, Generic[DataT]):
    count: int
    results: List[DataT]


class Pagination:
    def __init__(
        self,
        limit: int = Query(default=default_limit, ge=1, le=max_limit),
        offset: int = Query(default=default_offset, ge=0, le=max_offset),
        order_by: List[str] = Query(None),
    ):
        self.limit = limit
        self.offset = offset
        self.order_by = order_by

    async def paginate(self, qs: QuerySet):
        if self.order_by:
            try:
                qs = qs.order_by(*self.order_by)
            except FieldError as e:
                raise HTTPException(status_code=400, detail=str(e))
        count, results = await asyncio.gather(qs.count(), qs.limit(self.limit).offset(self.offset))

        return PaginationResult(count=count, results=results)
