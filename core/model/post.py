from datetime import datetime

from pydantic import Field

# from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from core.entity import Post
from core.enum import PostState
from core.model.board import BoardDefault
from core.model.user import UserSimple

from .base import Base

# PostModel = sqlalchemy_to_pydantic(Post)


class PostCreate(Base):
    title: str
    body: str
    writer_nick: str | None
    writer_id: int
    board_id: int


class PostUpdate(Base):
    title: str
    body: str
    id: int


class PostMeta(Base):
    id: int
    title: str
    writer_nick: str | None
    thumbnail: str | None
    view_cnt: int | None
    replies_cnt: int | None
    thumbs_up_cnt: int | None
    thumbs_down_cnt: int | None
    writer_id: int
    board_id: int
    board_name: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, obj: "PostMeta") -> "PostMeta":
        if hasattr(obj, "board"):
            obj.board_name = obj.board.name
        return super().from_orm(obj)


class PostMetaForBest(PostMeta):
    best_at: datetime | None


class PostReplyCreate(Base):
    target_id: int | None = None
    post_id: int
    writer_id: int
    writer_nick: str
    body: str


class PostReplyUpdate(Base):
    id: int
    body: str


class PostReplyDefault(PostReplyUpdate):
    created_at: datetime
    updated_at: datetime
    thumb: bool | None
    writer_id: int
    writer_nick: str
    thumbs_up_cnt: int
    thumbs_down_cnt: int

    replies: list["PostReplyDefault"]

    class Config:
        orm_mode = True


PostReplyDefault.update_forward_refs()


class PostDetail(PostMeta):
    body: str
    short_link: str | None
    state: PostState
    source: str | None

    thumb: bool | None

    writer: UserSimple | None = Field(None)
    board: BoardDefault
    replies: list[PostReplyDefault]
