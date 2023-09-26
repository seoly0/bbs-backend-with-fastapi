from core.entity import UserAccess

from .base import CRUDBase


class UserAccessCRUD(CRUDBase[UserAccess, None]):
    pass


user_access = UserAccessCRUD(UserAccess, None)
