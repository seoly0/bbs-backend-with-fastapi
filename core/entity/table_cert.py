from sqlalchemy import Column, DateTime, Enum, Integer, String

from core.enum import CertState, CertType

from .base import AuditMixin, BaseMixin, Entity


class CertBasic:
    type = Column(Enum(CertType))
    target_id = Column(Integer)
    key = Column(String(16))
    expire = Column(DateTime(timezone=True))
    state = Column(Enum(CertState), default=CertState.PENDING)


class Cert(Entity, BaseMixin, CertBasic):
    pass
