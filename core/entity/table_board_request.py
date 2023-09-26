from sqlalchemy import Column, Enum, Integer, String

from core.enum import BoardRequestState
from settings import CONST

from .base import AuditMixin, BaseMixin, Entity


class BoardRequestBasic:
    name = Column(String(CONST.BOARD_NAME_LENGTH))
    reason = Column(String(200))
    parent_id = Column(Integer, default=0)
    state = Column(Enum(BoardRequestState), default=BoardRequestState.PENDING)

    user_id = Column(Integer)
    user_nick = Column(String(CONST.HUMAN_NAME_LENGTH))

    cs_id = Column(Integer)
    cs_nick = Column(String(CONST.HUMAN_NAME_LENGTH))


class BoardRequest(Entity, BaseMixin, BoardRequestBasic):
    pass


class BoardRequestAud(Entity, AuditMixin, BoardRequestBasic):
    pass
