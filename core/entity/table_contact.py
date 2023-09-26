from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text

from core.enum import ContactState
from settings import CONST

from .base import AuditMixin, BaseMixin, Entity


class ContactBasic:
    category_id = Column(Integer)
    user_id = Column(Integer)
    user_nick = Column(String(CONST.HUMAN_NAME_LENGTH))

    cs_id = Column(Integer)
    cs_nick = Column(String(CONST.HUMAN_NAME_LENGTH))

    title = Column(String(CONST.POST_TITLE_LENGTH))
    content = Column(Text)
    answer = Column(Text)
    state = Column(Enum(ContactState), default=ContactState.PENDING)


class Contact(Entity, BaseMixin, ContactBasic):
    category_id = Column(Integer, ForeignKey("contact_category.id"))
    user_id = Column(Integer, ForeignKey("user.id"))


class ContactAud(Entity, AuditMixin, ContactBasic):
    pass
