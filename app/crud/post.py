from sqlalchemy import select, update
from sqlalchemy.orm import Session, joinedload

from core.entity import Post, PostAud, PostReply, PostReplyAud, Thumb

from .base import CRUDBase


def extract_ids(data: list[any]):
    ids = []
    for target in data:
        ids.append(target.id)
        if target.replies:
            ids = ids + extract_ids(target.replies)
    return ids


def reflect_thumbs(replies: list[PostReply], thumbs: list[Thumb]):
    for reply in replies:
        exist = list(filter(lambda x: x.reply_id == reply.id, thumbs))
        exist = exist[0] if len(exist) > 0 else None
        if exist:
            reply.thumb = exist.value

        if reply.replies:
            reflect_thumbs(reply.replies, thumbs)


class PostCRUD(CRUDBase[Post, PostAud]):
    @staticmethod
    def get_with(pid, uid, session: Session):
        result: Post = session.scalar(
            select(Post).where(Post.id == pid, Post.deleted == False)
            # .options(joinedload(Post.replies.and_(PostReply.target_id == None, PostReply.deleted == False)))
        )

        if result:
            if uid:
                post_thumbs = session.query(Thumb).filter(Thumb.user_id == uid, Thumb.post_id == pid).first()
                if post_thumbs:
                    result.thumb = post_thumbs.value

                ids = extract_ids(result.replies)
                replies_thumbs = session.query(Thumb).filter(Thumb.user_id == uid, Thumb.reply_id.in_(ids)).all()

                if replies_thumbs:
                    reflect_thumbs(result.replies, replies_thumbs)

        # TODO 베댓

        return result

    @staticmethod
    def increase_view_cnt(id, session: Session):
        query = update(Post).where(Post.id == id).values({Post.view_cnt: Post.view_cnt + 1})
        session.execute(query)
        return


class PostReplyCRUD(CRUDBase[PostReply, PostReplyAud]):
    @staticmethod
    def get_replies(pid, uid, session: Session):
        result = session.scalars(
            select(PostReply).where(PostReply.post_id == pid, PostReply.target_id == None, PostReply.deleted == False)
            # .where(PostReply.replies.)
            # .options(joinedload(PostReply.replies))  # TODO 대댓의 삭제여부체크 PostReply.deleted == False
        ).all()
        # result = (
        #     session.query(PostReply)
        #     .filter(PostReply.post_id == pid, PostReply.target_id == 0, PostReply.deleted == False)
        #     .options(joinedload(PostReply.replies))
        #     .all()
        # )

        if result:
            if uid:
                ids = extract_ids(result)
                # replies_thumbs = session.query(Thumb).filter(Thumb.user_id == uid, Thumb.reply_id.in_(ids)).all()
                replies_thumbs = session.scalars(
                    select(Thumb).where(Thumb.user_id == uid, Thumb.reply_id.in_(ids))
                ).all()
                if replies_thumbs:
                    reflect_thumbs(result, replies_thumbs)

        return result


post = PostCRUD(Post, PostAud)
post_reply = PostReplyCRUD(PostReply, PostReplyAud)
