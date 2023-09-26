from core.enum import NoticeType, NoticeState
from .base import Base


class NoticeCreate(Base):
    title: str
    body: str
    level: NoticeType
    writer_id: int
    writer_nick: str
    board_id: int


class NoticeUpdate(Base):
    id: int
    title: str
    body: str
    level: NoticeType


class NoticeToggleVisible(Base):
    id: int
    state: NoticeState
