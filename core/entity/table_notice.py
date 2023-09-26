from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text

from core.enum import NoticeState, NoticeType
from settings import CONST

from .base import AuditMixin, BaseMixin, Entity


class NoticeBasic:
    title = Column(String(CONST.POST_TITLE_LENGTH), nullable=False)
    body = Column(Text, nullable=False)
    level = Column(Enum(NoticeType))
    writer_nick = Column(String(CONST.HUMAN_NAME_LENGTH), nullable=False)

    writer_id = Column(Integer)
    board_id = Column(Integer)

    view_cnt = Column(Integer, default=0)

    state = Column(Enum(NoticeState), default=NoticeState.HIDDEN)


class Notice(Entity, BaseMixin, NoticeBasic):
    writer_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    board_id = Column(Integer, ForeignKey("board.id"), nullable=True)


class NoticeAud(Entity, AuditMixin, NoticeBasic):
    pass
