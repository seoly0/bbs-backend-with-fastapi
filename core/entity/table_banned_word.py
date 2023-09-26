from .base import Entity, BaseMixin, AuditMixin
from sqlalchemy import Column, String


class BannedWordbasic:

    word = Column(String(20), unique=True)


class BannedWord(Entity, BaseMixin, BannedWordbasic):
    pass
