from app.batch import app
from core.backend.postgres import SessionProvider
from core.entity import Mail
from core.enum import MailState

from .methods import send, send_bulk


@app.task(bind=True, default_retry_delay=5)
def mail_send(self, id: int):
    session = SessionProvider()
    pending: Mail = session.query(Mail).filter(Mail.id == id, Mail.state == MailState.PENDING).first()

    if pending is None:
        self.retry()
        return

    pending.state = MailState.PROCESSING
    session.add(pending)
    session.flush()
    session.commit()

    try:
        send(pending)

        pending.state = MailState.COMPLETE
        session.add(pending)

    except Exception as e:
        print(e)
        pending.state = MailState.FAIL
        session.add(pending)

    session.flush()
    session.commit()
    session.close()


@app.task
def retry_fail():
    session = SessionProvider()
    pending_list: list[Mail] = session.query(Mail).filter(Mail.id == id, Mail.state.is_(MailState.FAIL)).all()

    try:
        send_bulk(pending_list)

    except Exception:
        pass
