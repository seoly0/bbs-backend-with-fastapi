from core.enum import ContactState
from .base import Base


class ContactCategoryCreate(Base):
    name: str


class ContactCategoryUpdate(ContactCategoryCreate):
    id: int


class ContactCagegory(ContactCategoryUpdate):
    pass


class ContactCreate(Base):
    category_id: int
    user_id: int

    title: str
    content: str
    # answer: str


class ContactUpdate(Base):
    id: int

    title: str
    content: str


class ContactAnswer(Base):
    id: int
    answer: str
    cs_id: int | None
    cs_nick: str | None


class ContactUpdateState(Base):
    id: int
    state: ContactState

# class Contact(Base):
#     id: int
#     category_id: int
#     user_id: int

#     title: str
#     content: str
#     answer: str
