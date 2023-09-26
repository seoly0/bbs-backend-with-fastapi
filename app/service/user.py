from datetime import date, timedelta
from functools import reduce
from logging import getLogger

import bcrypt
from fastapi import Request
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from user_agents import parse

from app import crud
from core.auth import Authentication, issue
from core.entity import Cert, UserRole, UserTerms
from core.enum import CertState, CertType, UserRoleType, UserState
from core.exception import (AuthenticationFailException,
                            UserRegisterFailException)
from core.http.request import Request
from core.model.user import (UserAccessUpdate, UserAuthenticate,
                             UserAuthenticationContext, UserCreate,
                             UserCredentials, UserPasswordChange,
                             UserPasswordSet)
from libs.geographic import get_position_by_ip_address
from settings import ENV
from utils.strUtils import random_string
from utils.timeUtils import get_now

ENCODE = "utf-8"
logger = getLogger(__name__)


class UserService:
    @staticmethod
    def register(create: UserCreate, terms: list[int], session: Session):
        # TODO 유효성 검증
        # if create.nick and re.match('사용자-([0-9]*$)', create.nick):
        #     create.nick = None
        # 전화번호 검증 필요

        # 사용자 암호 인코딩
        en_pw = bcrypt.hashpw(create.password.encode(ENCODE), bcrypt.gensalt()).decode(ENCODE)
        create.password = en_pw

        # 사용자 생성
        try:
            new_user = crud.user.create(create, session)
        except IntegrityError as e:
            msg = str(e)
            print(msg)
            if msg.find("user.email") > -1:
                raise UserRegisterFailException("이미 사용중인 이메일입니다.")
            elif msg.find("user.nick") > -1:
                raise UserRegisterFailException("이미 사용중인 닉네임입니다.")
            else:
                raise UserRegisterFailException("회원가입에 실패했습니다.")

        # 약관 동의
        UserService.agree(new_user.id, terms, session)

        # 롤 생성
        role = UserRole(user_id=new_user.id, type=UserRoleType.USER)
        crud.user_role.create(role, session)
        new_user = crud.user.get(new_user.id, session)
        # new_user.roles = [role]

        # 인증토큰 발급
        cert = Cert()
        cert.type = CertType.USER_JOIN
        cert.key = random_string(16)
        cert.expire = get_now() + timedelta(hours=1)
        cert.target_id = new_user.id
        session.add(cert)
        session.flush()

        # 메일 등록
        crud.mail.create(
            {
                "target": new_user.email,
                "title": "회원가입인증",
                "template": "CertJoin.html",
                "context": str({"key": f"{ENV.WEB_HOST}/cert?key={cert.key}"}),
            },
            session,
        )

        return new_user

    @staticmethod
    def cert_again(uid: int, session):
        # 기존 인증토큰 비활성화
        old_cert: Cert = (
            session.query(Cert)
            .filter(Cert.target_id.is_(uid), Cert.type.is_(CertType.USER_JOIN), Cert.state.is_(CertState.PENDING))
            .first()
        )
        if old_cert:
            old_cert.state = CertState.CANCELED
            session.add(old_cert)
            session.flush()

        # 새 인증토큰 발급
        new_cert = Cert()
        new_cert.type = CertType.USER_JOIN
        new_cert.key = random_string(16)
        new_cert.expire = get_now() + timedelta(hours=1)
        new_cert.target_id = uid

        session.add(new_cert)
        session.flush()

        user = crud.user.get(uid, session)

        # 메일 등록
        crud.mail.create(
            {
                "target": user.email,
                "title": "회원가입인증",
                "template": "CertJoin.html",
                "context": str({"key": f"{ENV.WEB_HOST}/cert?key={new_cert.key}"}),
            },
            session,
        )

        return True

    @staticmethod
    def agree(uid: int, terms: list[int], session):
        terms = map(lambda x: UserTerms(user_id=uid, terms_id=x), terms)
        for t in terms:
            crud.user_terms.create(t, session)

        return True

    @staticmethod
    def authenticate(
        user: UserAuthenticate,
        request: Request,
        user_agent: str,
    ):
        session = request.state.backend
        target = crud.user.get_by_email(user.email, session)

        # 사용자가 없음
        if target is None:
            raise AuthenticationFailException

        # 암호 일치 확인
        verified = bcrypt.checkpw(user.password.encode(ENCODE), target.password.encode(ENCODE))

        # 비밀번호가 일치하지 않음
        if verified is False:
            raise AuthenticationFailException

        # 액세스토큰 발급
        roles = list(map(lambda x: x.type.value, target.roles))
        auth = Authentication(id=target.id, email=target.email, roles=roles, extra={"nick": target.nick})
        access_token = issue(auth)

        #
        credentials = UserCredentials()

        #
        context = UserAuthenticationContext(credentials=credentials)
        context.user = target

        # ACTIVE 체크 (기본값 PENDING, 이메일 인증을 완료하지 않음)
        if target.state != UserState.ACTIVE:
            # 토큰을 발급하지 않음, 이메일 인증 안내 페이지로 리다이렉트
            context.redirect = "이메일인증"
            return context

        # TODO 라스트 엑세스 체크 -> 메일..?

        # 여기서부턴 토큰을 발급함
        context.credentials.access_token = access_token

        # 최신 버전의 약관 동의 여부 확인
        required = crud.terms.get_required(session)
        agreed = crud.user_terms.get_agreed_by(target.id, session)
        result = True
        for terms_id in required:
            result = result and reduce(lambda x, y: x or y.terms_id == terms_id, agreed, False)
        if not result:
            context.redirect = "최신약관동의"
            return context

        # 마지막 비밀번호 변경으로부터 90일 이상 지남
        diff = date.today() - target.password_last_changed.date()
        if diff.days > 90:
            # 토큰을 발급함, 비밀번호 변경 안내 페이지로 리다이렉트
            context.redirect = "비밀번호변경"
            return context

        # 아무 이상 없음
        return context

    # 왜 있는거지...?
    # 회원가입할때 중복때문에?
    # @staticmethod
    # def find_email():
    #     pass

    @staticmethod
    def available_nick(nick: str, session):
        result = crud.user.get_by_nick(nick, session)
        return result is None

    @staticmethod
    def send_cert_password_reset(email, session):
        user = crud.user.get_by_email(email, session)

        # 인증토큰 발급
        cert = Cert()
        cert.type = CertType.USER_PWRESET
        cert.key = random_string(16)
        cert.expire = get_now() + timedelta(hours=1)
        cert.target_id = user.id
        session.add(cert)
        session.flush()

        # 메일 등록
        crud.mail.create(
            {
                "target": user.email,
                "title": "비밀번호변경",
                "template": "CertJoin.html",
                "context": str({"key": f"{ENV.WEB_HOST}/cert?key={cert.key}"}),
            },
            session,
        )

        return True

    @staticmethod
    def change_password(id: int, reset: UserPasswordChange | None, session):
        """
        - reset Exist : 비밀번호를 변경하며 password_last_changed 필드를 갱신함
        - reset None  : 비밀번호를 변경하지 않으며 password_last_changed 필드를 갱신함
        """

        user = crud.user.get(id, session)

        # auth 체크를 먼저 하기 때문에 발생하지 않을 예외
        # TODO 꼭 그렇지 않을수도 있겠네 (차단이나 회원탈퇴 등도 판단해야함.)
        if user is None:
            return False

        if reset is not None:
            verified = bcrypt.checkpw(reset.old.encode(ENCODE), user.password.encode(ENCODE))

            # 암호는 틀릴수 있으니 충분히 발생할 수 있는 예외
            if verified is False:
                return False

            set = UserPasswordSet(
                id=id,
                password=bcrypt.hashpw(reset.new.encode(ENCODE), bcrypt.gensalt()),
                password_last_changed=func.now(),
            )
        else:
            set = UserPasswordSet(id=id, password=user.password, password_last_changed=func.now())

        crud.user.update(set, session)
        return True

    @staticmethod
    def patch_nick(update, session, id):
        return crud.user.update(update=update, session=session, check=("id", id))

    # @staticmethod
    # def issue_tmp_password():
    #     pass
    #
    # @staticmethod
    # def activate_user():
    #     pass
    #
    # @staticmethod
    # def block_user():
    #     pass


user = UserService()
