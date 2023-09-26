from .base import Entity, BaseMixin, AuditMixin
from sqlalchemy import Column, String, Text, Integer, Boolean


class AlertBasic:
    user_id = Column(Integer)
    title = Column(String)
    type = Column(String)
    content = Column(Text)
    link = Column(String)
    read = Column(Boolean)
    deleted = Column(Boolean)


class Alert(Entity, BaseMixin, AlertBasic):
    pass


class AlertAud(Entity, AuditMixin, AlertBasic):
    pass
