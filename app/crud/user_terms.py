from sqlalchemy import select
from sqlalchemy.orm import Session

from core.entity import UserTerms, UserTermsAud

from .base import CRUDBase


class UserTermsCRUD(CRUDBase[UserTerms, UserTermsAud]):
    @staticmethod
    def get_agreed_by(uid, session: Session) -> list[UserTerms]:
        return session.scalars(select(UserTerms).where(UserTerms.user_id == uid)).all()


user_terms = UserTermsCRUD(UserTerms, UserTermsAud)
