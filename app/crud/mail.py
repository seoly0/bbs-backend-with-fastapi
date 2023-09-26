from sqlalchemy.orm import Session

from app.batch.mail.tasks import mail_send
from core.entity import Mail
from core.model.mail import MailCreate

from .base import CRUDBase


class MailCRUD(CRUDBase[Mail, None]):
    def create(self, create: MailCreate, session: Session) -> Mail:
        # DB 등록
        obj = super().create(create, session)

        # 메일발송
        mail_send.delay(obj.id)

        return obj


mail = MailCRUD(Mail, None)
