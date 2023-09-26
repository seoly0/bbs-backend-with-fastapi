from .base import Entity, BaseMixin, AuditMixin
from sqlalchemy import Column, ForeignKey, Enum, Integer
from core.enum import UserRoleType


class UserRoleBasic:
    user_id = Column(Integer)
    type = Column(Enum(UserRoleType))


class UserRole(Entity, BaseMixin, UserRoleBasic):
    user_id = Column(Integer, ForeignKey("user.id"))


class UserRoleAud(Entity, AuditMixin, UserRoleBasic):
    pass
