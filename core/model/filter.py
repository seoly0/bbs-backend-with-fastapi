from .base import Base


class Page(Base):
    page: int = 1
    size: int = 10
    order: str | None = None  # created_at,id
