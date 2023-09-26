from logging import getLogger

import bcrypt
from sqlalchemy import insert, select, text

from core.backend.postgres import SessionProvider
from core.entity import Board, User, UserRole
from core.enum import UserRoleType, UserState
from settings import ENV

from .base import BootBase

logger = getLogger(__name__)


class DatebaseBoot(BootBase):
    def verify(self):
        logger.debug("데이터베이스 연결 테스트")
        try:
            session = SessionProvider()
            session.execute(text("SELECT 1"))
            logger.debug("데이터베이스 연결 테스트 통과")
            session.close()
            return True
        except Exception as e:
            logger.error("데이터베이스 연결 테스트 실패")
            logger.error(e)
            return False

    def execute(self):
        session = SessionProvider()
        session.commit()
        session.close()


boot = DatebaseBoot()
order = 3
