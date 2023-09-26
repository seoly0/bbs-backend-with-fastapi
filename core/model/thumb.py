from .base import Base


class ThumbDefault(Base):
    user_id: int
    post_id: int | None
    reply_id: int | None

    value: bool
