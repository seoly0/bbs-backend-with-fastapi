from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.enum import PostState
from settings import CONST

from .base import AuditMixin, BaseMixin, Entity


class PostReplyBasic:
    post_id = Column(Integer)
    target_id = Column(Integer)
    writer_id = Column(Integer)
    writer_nick = Column(String(CONST.HUMAN_NAME_LENGTH), nullable=False)

    body = Column(String(300))

    state = Column(Enum(PostState), default=PostState.ACTIVE)

    best = Column(Boolean, default=False)
    best_at = Column(DateTime(timezone=True), nullable=True)

    thumbs_up_cnt = Column(Integer, default=0)
    thumbs_down_cnt = Column(Integer, default=0)


class PostReply(Entity, BaseMixin, PostReplyBasic):
    target_id = Column(Integer, ForeignKey("post_reply.id"), nullable=True)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    writer_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    replies = relationship(
        "PostReply",
        lazy="joined",
        join_depth=2,
        primaryjoin="and_(post_reply.c.id == remote(PostReply.target_id), remote(PostReply.deleted)==False)",
        order_by="PostReply.created_at.asc()",
    )

    thumb: bool | None = None


class PostReplyAud(Entity, AuditMixin, PostReplyBasic):
    pass
