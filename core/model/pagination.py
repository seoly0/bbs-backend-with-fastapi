# https://github.com/uriyyo/fastapi-pagination

from pydantic.generics import GenericModel
from typing import TypeVar, Generic

# from .base import Base

ContentType = TypeVar("ContentType")


class Pagination(GenericModel, Generic[ContentType]):
    contents: list[ContentType]
    page: int  # 현재 페이지, 1부터 시작
    size: int  # 한 페이지 당 요소 크기
    total: int  # 전체 요소 크기
    pages: int  # 전체 페이지 크기

    # def create(self, query: Query, offset: int = 0, size: int = 10):  # order: str | None = None
    #
    #     return self(
    #         contents=query.offset(offset).limit(size).all(),
    #         offset=offset,
    #         size=size,
    #         total=query.count(),
    #         pages=1 + self.total // size
    #     )

    class Config:
        arbitrary_types_allowed = True


__all__ = ["Pagination"]
