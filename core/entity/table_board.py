from sqlalchemy import Boolean, Column, Enum, Integer, String

from core.enum import BoardState
from settings import CONST

from .base import AuditMixin, BaseMixin, Entity


class BoardBasic:
    name = Column(String(CONST.BOARD_NAME_LENGTH))
    parent_id = Column(Integer)
    state = Column(Enum(BoardState), default=BoardState.ACTIVE)
    select_best = Column(Boolean, default=True)


class Board(Entity, BaseMixin, BoardBasic):
    pass


class BoardAud(Entity, AuditMixin, BoardBasic):
    pass
