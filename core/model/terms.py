from .base import Base


class TermsCreate(Base):
    content: str
    type: str
    version: int


class TermsUpdate(Base):
    id: int
    content: str
