from sqlalchemy import Column, ForeignKey, Integer, String

from .base import BaseMixin, Entity


class UserAccessBasic:
    user_id = Column(Integer)
    ip = Column(String(15))
    where = Column(String(50))
    device = Column(String(150))


class UserAccess(Entity, BaseMixin, UserAccessBasic):
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
