from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from core.enum import PostState
from settings import CONST

from .base import AuditMixin, BaseMixin, Entity


class PostBasic:
    title = Column(String(CONST.POST_TITLE_LENGTH), nullable=False)
    body = Column(Text, nullable=False)
    body_plain = Column(Text, nullable=False)
    writer_nick = Column(String(CONST.HUMAN_NAME_LENGTH), nullable=False)
    thumbnail = Column(String(CONST.MEDIA_URI_LENGTH))

    writer_id = Column(Integer)
    board_id = Column(Integer)

    best = Column(Boolean, default=False)
    best_at = Column(DateTime(timezone=True), nullable=True)

    view_cnt = Column(Integer, default=0)
    replies_cnt = Column(Integer, default=0)
    thumbs_up_cnt = Column(Integer, default=0)
    thumbs_down_cnt = Column(Integer, default=0)

    state = Column(Enum(PostState), default=PostState.ACTIVE)

    short_link = Column(String(CONST.URL_SHORT_LENGTH))
    soruce = Column(String(CONST.URL_LENGTH))


class Post(Entity, BaseMixin, PostBasic):
    writer_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    board_id = Column(Integer, ForeignKey("board.id"), nullable=False)

    writer = relationship("User")
    board = relationship("Board")
    replies = relationship(
        "PostReply",
        primaryjoin="and_(Post.id == PostReply.post_id, PostReply.deleted == False, PostReply.target_id == None)",
        order_by="PostReply.created_at.asc()",
    )

    thumb: bool | None = None


class PostAud(Entity, AuditMixin, PostBasic):
    pass
