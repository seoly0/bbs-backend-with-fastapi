from sqlalchemy import Column, DateTime, Enum, String, func
from sqlalchemy.orm import relationship

from core.enum import UserState
from settings import CONST

from .base import AuditMixin, BaseMixin, Entity


class UserAuthentication:
    # 인즐정보
    email = Column(String(100), unique=True, index=True)
    email_lock = Column(String(100))
    password = Column(String(100))
    password_tmp = Column(String(100))
    password_last_changed = Column(DateTime(timezone=True), server_default=func.now())


class UserPrivateRequiredInfo:
    # 개인정보(필수)
    name = Column(String(CONST.HUMAN_NAME_LENGTH))

    # 본인인증 정보가 포함될수도 있음
    # 전화번호 성별 등


class UserPrivateOptionalInfo:
    # 개인정보(선택)
    phone = Column(String(CONST.PHONE_NUMBER_LENGTH))  # 본인인증시 필수정보일 수 있음. 잘 모름.
    zipcode = Column(String(10))
    address = Column(String(100))
    address_detail = Column(String(100))


class UserPublicRequiredInfo:
    # 공개정보(필수)
    nick = Column(String(CONST.HUMAN_NAME_LENGTH), unique=True)


class UserPublicOptionalInfo:
    # 공개정보(선택)
    introduction = Column(String(200), default="안녕하세요. 잘 부탁드립니다.")
    thumbnail = Column(String(CONST.MEDIA_URI_LENGTH))


class UserManagement:
    # 접근정보
    # last_access_ip = Column(String(15))
    # last_access_when = Column(DateTime(timezone=True))
    # last_access_where = Column(String(50))
    # last_access_device = Column(String(150))

    # 상태정보
    state = Column(Enum(UserState), default=UserState.PENDING)


class UserBasic(
    UserAuthentication,
    UserPrivateRequiredInfo,
    UserPrivateOptionalInfo,
    UserPublicRequiredInfo,
    UserPublicOptionalInfo,
    UserManagement,
):
    pass


class User(Entity, BaseMixin, UserBasic):
    roles = relationship("UserRole")
    access = relationship("UserAccess")


class UserAud(Entity, AuditMixin, UserBasic):
    pass
