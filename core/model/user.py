from datetime import datetime
from typing import Any

from pydantic import EmailStr, Field, validator

from core.enum import UserRoleType, UserState

from .base import Base, media_url_composite


class UserRole(Base):
    type: UserRoleType

    class Config:
        orm_mode = True


class UserTerms(Base):
    user_id: int
    terms_id: int


class UserSimple(Base):
    id: int = None
    nick: str
    introduction: str | None
    thumbnail: str | None

    _thumbnail = validator("thumbnail", allow_reuse=True)(media_url_composite)

    class Config:
        orm_mode = True


class UserDefault(Base):
    id: int = None
    email: EmailStr
    state: UserState
    nick: str
    name: str
    # job: str | None
    introduction: str | None
    thumbnail: str | None

    created_at: datetime
    updated_at: datetime

    _thumbnail = validator("thumbnail", allow_reuse=True)(media_url_composite)

    class Config:
        orm_mode = True


UserDefault.update_forward_refs()


class UserWithRole(UserDefault):
    roles: list[UserRole] = []


class UserCreate(Base):
    email: EmailStr
    password: str
    name: str = Field(example="홍길동")
    nick: str = Field(example="shyHong")
    phone: str | None = Field(example="010-0000-0000")
    zipcode: str | None
    address: str | None
    address_detail: str | None


class UserAccessUpdate(Base):
    id: int
    last_access_ip: str | None
    last_access_when: Any | None
    last_access_where: str | None
    last_access_device: str | None


class UserNickUpdate(Base):
    id: int
    nick: str


class UserThumbnailUpdate(Base):
    id: int
    thumbnail: str


class UserExtraUpdate(Base):
    id: int
    # job: str | None
    introduction: str | None


class UserStateUpdate(Base):
    id: int
    state: UserState


class UserAuthenticate(Base):
    email: str
    password: str


class UserCredentials(Base):
    access_token: str | None
    refresh_token: str | None


class UserAuthenticationContext(Base):
    user: UserDefault | None
    credentials: UserCredentials | None
    redirect: str | None
    extra: Any


class UserPasswordChange(Base):
    old: str
    new: str


class UserPasswordSet(Base):
    id: int
    password: str
    password_last_changed: Any


class UserRoleCreate(Base):
    user_id: int
    type: str
