from core.entity import Thumb, ThumbAud

from .base import CRUDBase


class ThumbCRUD(CRUDBase[Thumb, ThumbAud]):
    pass


thumb = ThumbCRUD(Thumb, ThumbAud)
