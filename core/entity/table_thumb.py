from .base import Entity, BaseMixin, AuditMixin
from sqlalchemy import Column, Boolean, Integer


class ThumbBasic:
    user_id = Column(Integer)
    post_id = Column(Integer)
    reply_id = Column(Integer)

    value = Column(Boolean, default=False)


class Thumb(Entity, BaseMixin, ThumbBasic):
    pass


class ThumbAud(Entity, AuditMixin, ThumbBasic):
    pass
