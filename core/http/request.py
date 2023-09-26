from typing import Generic, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel
from sqlalchemy.orm import Session
from starlette.requests import Request as StarletteRequest

from core.auth import Authentication


class State:
    backend: Session
    auth: Authentication


class Request(StarletteRequest):
    @property
    def state(self) -> State:
        return super().state


ContentType = TypeVar("ContentType")


class Pagination(GenericModel, Generic[ContentType]):
    contents: list[ContentType]
    page: int  # 현재 페이지, 1부터 시작
    size: int  # 한 페이지 당 요소 크기
    total: int  # 전체 요소 크기
    pages: int  # 전체 페이지 크기

    class Config:
        arbitrary_types_allowed = True


class Page(BaseModel):
    page: int = 1
    size: int = 10
    order: str | None = None
