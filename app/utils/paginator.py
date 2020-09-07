import pydantic


class LimitOffsetPagination(pydantic.BaseModel):
    limit: int
    offset: int


async def limit_offset_paginator(limit: int = 10, offset: int = 0):
    print(limit, offset)
    return LimitOffsetPagination(limit=limit, offset=offset)
