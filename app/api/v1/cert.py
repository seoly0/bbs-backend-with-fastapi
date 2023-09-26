import bcrypt
from fastapi import APIRouter
from sqlalchemy import func, select

from app import crud
from core.entity import Cert
from core.enum import CertState, CertType, UserState
from core.http.request import Request
from core.model.user import UserPasswordSet, UserStateUpdate
from utils.timeUtils import get_now

router = APIRouter()
router.tags = ["인증"]
router.prefix = "/cert"


@router.post("")
def do_cert(req: Request, key: str, params: dict = None):
    session = req.state.backend

    # cert: Cert = session.query(Cert).filter(Cert.key == key, Cert.state == CertState.PENDING).first()
    cert = session.scalar(select(Cert).where(Cert.key == key, Cert.state == CertState.PENDING))

    if cert is None:
        # print('토큰이 없음')
        return False

    if get_now() > cert.expire:
        # print('토큰이 만료됨')
        return False

    # 액션
    # 회원가입 이메일 인증
    if cert.type == CertType.USER_JOIN:
        update = UserStateUpdate(id=cert.target_id, state=UserState.ACTIVE)
        crud.user.update(update=update, session=session)

    # 비밀번호 재설정
    elif cert.type == CertType.USER_PWRESET:
        en_pw = bcrypt.hashpw(params.get("password").encode("utf-8"), bcrypt.gensalt())
        update = UserPasswordSet(id=cert.target_id, password=en_pw, password_last_changed=func.now())
        crud.user.update(update=update, session=session)

    cert.state = CertState.COMPLETE
    session.add(cert)

    return True
