from typing import Optional

from pydantic import EmailStr
from sqlalchemy.orm import Session, joinedload

from core.entity import User, UserAud

from .base import CRUDBase


class UserCRUD(CRUDBase[User, UserAud]):
    @staticmethod
    def get_with_roles(id, session: Session) -> Optional[User]:
        result = (
            session.query(User).filter(User.id == id, User.deleted == False).options(joinedload(User.roles)).first()
        )

        return result

    # @staticmethod
    # def get_with_members(id, session: Session) -> Optional[User]:
    #     result = session.query(User) \
    #         .filter(User.id == id) \
    #         .options(joinedload(User.members)) \
    #         .first()
    #
    #     return result

    @staticmethod
    def get_by_email(email: EmailStr, session: Session) -> Optional[User]:  # noqa
        result = (
            session.query(User)
            .filter(User.email == email, User.deleted == False)
            .options(joinedload(User.roles))
            .first()
        )

        return result

    @staticmethod
    def get_by_nick(nick: str, session: Session) -> Optional[User]:  # noqa
        result = session.query(User).filter(User.nick == nick, User.deleted.is_(False)).first()

        return result


user = UserCRUD(User, UserAud)
