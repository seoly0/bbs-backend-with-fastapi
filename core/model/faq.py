from typing import Optional
from .base import Base


class FAQCreate(Base):
    title: Optional[str]
    content: Optional[str]
    order: Optional[int]
    show: Optional[bool]


class FAQUpdate(FAQCreate):
    id: int = None


class FAQUpdateShow(Base):
    id: int
    show: bool


class FAQDefault(FAQUpdate):
    class Config:
        orm_mode = True
