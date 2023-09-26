from pydantic import EmailStr
from .base import Base


class MailCreate(Base):
    target: EmailStr
    title: str
    template: str
    content: str
