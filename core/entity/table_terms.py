from .base import Entity, BaseMixin, AuditMixin
from sqlalchemy import Column, String, Text, Integer


class TermsBasic:
    content = Column(Text)
    type = Column(String)
    version = Column(Integer)


class Terms(Entity, BaseMixin, TermsBasic):
    pass


class TermsAud(Entity, AuditMixin, TermsBasic):
    pass
