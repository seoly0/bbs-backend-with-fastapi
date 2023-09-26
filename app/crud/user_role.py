from .base import CRUDBase
from core.entity import UserRole, UserRoleAud


class UserRoleCRUD(CRUDBase[UserRole, UserRoleAud]):
    pass


user_role = UserRoleCRUD(UserRole, UserRoleAud)
