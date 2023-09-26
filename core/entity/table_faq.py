from .base import Entity, BaseMixin, AuditMixin
from sqlalchemy import Column, String, Text, Integer, Boolean


class FaqBasic:
    title = Column(String(100))
    content = Column(Text)
    order = Column(Integer)
    show = Column(Boolean)


class Faq(Entity, BaseMixin, FaqBasic):
    pass


class FaqAud(Entity, AuditMixin, FaqBasic):
    pass
