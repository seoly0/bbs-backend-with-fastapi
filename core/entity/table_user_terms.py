from .base import Entity, BaseMixin, AuditMixin
from sqlalchemy import Column, ForeignKey, Integer


class UserTermsBasic:
    user_id = Column(Integer)
    terms_id = Column(Integer)


class UserTerms(Entity, BaseMixin, UserTermsBasic):
    user_id = Column(Integer, ForeignKey('user.id'))
    terms_id = Column(Integer, ForeignKey('terms.id'))


class UserTermsAud(Entity, AuditMixin, UserTermsBasic):
    pass
