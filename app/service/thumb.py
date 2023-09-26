from datetime import datetime, timedelta

from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from core.entity import Post, PostReply, Thumb
from core.model.thumb import ThumbDefault
from utils.timeUtils import get_now


class ThumbService:
    @staticmethod
    def reflect(thumb: ThumbDefault, uid: int, session: Session):
        # 권한 체크 및 uid 위조방지
        thumb.user_id = uid

        try:
            # 따봉 내역이 존재하는지 여부 조사
            t: Thumb = (
                session.query(Thumb)
                .filter(
                    Thumb.user_id == thumb.user_id,
                    or_(
                        # == 0 조건은 게시글과 댓글의 따봉을 한 테이블에서 관리하기 때문에 꼭 필요
                        and_(Thumb.post_id == thumb.post_id, Thumb.reply_id == 0),
                        and_(Thumb.reply_id == thumb.reply_id, Thumb.post_id == 0),
                    ),
                )
                .first()
            )
            # 테스트로 베스트 보내고자 할땐 t에 None을 할당

            # 내역이 존재하지 않는다면 생성
            if t is None:
                t = Thumb()
                t.user_id = thumb.user_id
                t.post_id = thumb.post_id
                t.reply_id = thumb.reply_id
                t.value = thumb.value

            # 내역이 존재할 때
            else:
                # 기존값과 새 값이 같다면 -> 삭제
                if t.value == thumb.value:
                    session.delete(t)
                    return True
                # 기존값과 다르다면 -> 변경
                else:
                    t.value = thumb.value

            # 디비에 반영
            session.add(t)
            session.flush()
            session.refresh(t)

            # post 혹은 reply에 값 반영
            if thumb.post_id:
                u_count = session.query(Thumb).filter(Thumb.post_id == thumb.post_id, Thumb.value == True).count()
                d_count = session.query(Thumb).filter(Thumb.post_id == thumb.post_id, Thumb.value == False).count()
                post: Post = session.query(Post).get(thumb.post_id)
                post.thumbs_up_cnt = u_count
                post.thumbs_down_cnt = d_count

                # 베스트 게시글
                if not post.best and post.thumbs_up_cnt >= 5 and get_now() - post.created_at < timedelta(hours=24):
                    post.best = True
                    post.best_at = func.now()

                session.add(post)
                session.flush()

            elif thumb.reply_id:
                u_count = session.query(Thumb).filter(Thumb.reply_id == thumb.reply_id, Thumb.value == True).count()
                d_count = session.query(Thumb).filter(Thumb.reply_id == thumb.reply_id, Thumb.value == False).count()
                reply: PostReply = session.query(PostReply).get(thumb.reply_id)
                reply.thumbs_up_cnt = u_count
                reply.thumbs_down_cnt = d_count

                # TODO 베스트 댓글

                session.add(reply)
                session.flush()

        except Exception as e:
            print(e)
            return False

        return True


thumb = ThumbService()
