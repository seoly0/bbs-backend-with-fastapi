from .base import CRUDBase
from core.entity import BannedWord


class BannedWordCRUD(CRUDBase[BannedWord, None]):
    pass


banned_word = BannedWordCRUD(BannedWord, None)
