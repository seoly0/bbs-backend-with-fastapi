from sqlalchemy import select
from sqlalchemy.orm import Session

from core.entity import Faq, FaqAud

from .base import CRUDBase

# from core.schemas.faq import FAQCreate, FAQUpdate


class FaqCRUD(CRUDBase[Faq, FaqAud]):
    # def get_list(self, session):
    #     result = session.query(Faq).filter(Faq.deleted == False).order_by(desc(Faq.order)).all()
    #     return result

    @staticmethod
    def get_visible_list(session: Session):
        return session.scalars(
            select(Faq).where(Faq.deleted == False, Faq.show == True).order_by(Faq.order.desc())
        ).all()


faq = FaqCRUD(Faq, FaqAud)
