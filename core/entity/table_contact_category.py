from .base import Entity, BaseMixin, AuditMixin
from sqlalchemy import Column, String


class ContactCategoryBasic:
    name = Column(String(10))


class ContactCategory(Entity, BaseMixin, ContactCategoryBasic):
    pass


class ContactCategoryAud(Entity, AuditMixin, ContactCategoryBasic):
    pass
