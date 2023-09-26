from sqlalchemy import Column, Enum, Integer, String, Text

from core.enum import MailState

from .base import AuditMixin, BaseMixin, Entity


class MailBasic:
    # type = Column(String)  # 메일 유형
    template = Column(String(50))  # 메일 템플릿
    target = Column(String)  # 대상 이메일
    title = Column(String(100))
    context = Column(Text)

    user_id = Column(Integer)  # 대상 유저 아이디
    sender_id = Column(Integer, default=0)  # 보낸 유저 아이디 (0: system, 1~: 관리자)

    state = Column(Enum(MailState), default=MailState.PENDING)


class Mail(Entity, BaseMixin, MailBasic):
    pass
