from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, aliased

from core.entity import Terms, TermsAud

from .base import CRUDBase

# from core.schemas.terms import TermsCreate


class TermsCRUD(CRUDBase[Terms, TermsAud]):
    @staticmethod
    def get_service(session: Session) -> Terms:
        return session.scalar(
            select(Terms).where(Terms.type == "SERVICE", Terms.deleted == False).order_by(Terms.version.desc())
        )

    @staticmethod
    def get_privacy(session: Session) -> Terms:
        return session.scalar(
            select(Terms).where(Terms.type == "PRIVACY", Terms.deleted == False).order_by(Terms.version.desc())
        )

    @staticmethod
    def get_required(session: Session):
        subquery = select(
            Terms, func.rank().over(partition_by=Terms.type, order_by=Terms.version.desc()).label("latest")
        ).where(or_(Terms.type == "SERVICE", Terms.type == "PRIVACY"))
        query = select(subquery.c.id).select_from(subquery).where(subquery.c.latest == 1)
        result = session.scalars(query).all()

        return result


terms = TermsCRUD(Terms, TermsAud)
