from sqlalchemy import select
from sqlalchemy.orm import Session

from core.entity import Notice, NoticeAud
from core.enum import NoticeType

from .base import CRUDBase

# from core.schemas.notice import NoticeCreate


class NoticeCRUD(CRUDBase[Notice, NoticeAud]):
    @staticmethod
    def get_important_list(session: Session):
        return session.scalars(
            select(Notice).where(Notice.deleted == False, Notice.level == NoticeType.IMPORTANT)
        ).all()


notice = NoticeCRUD(Notice, NoticeAud)
