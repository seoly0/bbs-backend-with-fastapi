import datetime
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Header, UploadFile

from app import crud, service
from core.auth import has_role
from core.exception import MIMETypeException
from core.http.request import Request
from core.http.response import Response
from core.model.user import (UserAuthenticate, UserAuthenticationContext,
                             UserCreate, UserDefault, UserExtraUpdate,
                             UserNickUpdate, UserPasswordChange,
                             UserThumbnailUpdate)
from libs.media import save

router = APIRouter()
router.tags = ["사용자"]
router.prefix = "/user"


@router.get(
    path="/info",
    name="사용자 정보",
    response_model=UserDefault,
)
@has_role(["USER"])
def serve_info(req: Request):
    return crud.user.get_with_roles(req.state.auth.id, req.state.backend)


@router.get(
    path="/info/{user_id}",
    name="사용자 정보",
    response_model=UserDefault,
)
def serve_info(req: Request, user_id):
    return crud.user.get(user_id, req.state.backend)


@router.post(path="/register", name="회원가입", response_model=UserDefault)
def register_user(request: Request, create: UserCreate, terms: list[int]):
    return service.user.register(create, terms, request.state.backend)


@router.get(path="/available", name="닉네임 유일값 사용 가능 여부")
def check_available(req: Request, nick: str):
    return service.user.available_nick(nick, req.state.backend)


@router.post(path="/register/cert", name="인증 이메일 재발송")
def register_cert(req: Request, id: int):
    service.user.cert_again(id, req.state.backend)
    return True


@router.post(path="/terms", name="약관동의")
@has_role(["USER"])
def terms_agree(req: Request, terms: list[int]):
    return service.user.agree(req.state.auth.id, terms, req.state.backend)


@router.post(path="/authenticate", name="로그인", response_model=UserAuthenticationContext)
def authenticate_user(
    req: Request,
    res: Response,
    user: UserAuthenticate,
    secure: Optional[bool] = None,
    user_agent: str | None = Header(default=None),
):
    if secure is None:
        secure = True

    context = service.user.authenticate(
        user=user,
        request=req,
        user_agent=user_agent,
    )

    # 쿠키 설정
    res.set_cookie(
        key="access_token",
        value=context.credentials.access_token,
        max_age=60 * 60 * 24 * 30,
        secure=secure,
        httponly=secure,
        samesite="None",
    )

    return context


@router.put(path="/info", name="사용자 정보 수정", response_model=UserDefault)
@has_role(["USER"])
def update_user_info(req: Request, update: UserExtraUpdate):
    update.id = req.state.auth.id
    return crud.user.update(update=update, session=req.state.backend)


@router.patch(
    path="/nick",
    name="닉네임 변경",
    response_model=UserDefault,
)
@has_role(["USER"])
def patch_nick(req: Request, update: UserNickUpdate):
    update.id = req.state.auth.id
    return service.user.patch_nick(update=update, session=req.state.backend, id=req.state.auth.id)


@router.patch(
    path="/thumbnail",
    name="썸네일 변경",
    response_model=UserDefault,
)
@has_role(["USER"])
def patch_thumbnail(req: Request, image: UploadFile):
    mime = image.content_type.split("/")[0]
    ext = image.content_type.split("/")[1]

    if mime != "image":
        raise MIMETypeException("이미지 형식의 파일이 아닙니다.")

    path = f"thumbnail/user/{datetime.date.today()}_{req.state.auth.id}_{uuid4()}.{ext}"

    update = UserThumbnailUpdate(id=req.state.auth.id, thumbnail=path)
    result = crud.user.update(update=update, session=req.state.backend, check=("id", req.state.auth.id))

    # 파일저장과 db저장 순서가 논리적으로 상관없어 보이나, 파일저장 후 db저장시 미들웨어 단에서 commit error 발생(disk io error)
    # 원인 파악 필요
    save(path=path, file=image.file.fileno())

    return result


@router.patch(path="/password/reset", name="비밀번호 재설정 인증메일 보내기")
def reset_password(req: Request, email):
    service.user.send_cert_password_reset(email, req.state.backend)
    return True


@router.patch(path="/password/change", name="비밀번호 변경")
@has_role(["USER"])
def change_password(
    req: Request,
    reset: UserPasswordChange,
):
    """
    인증을 얻은 상태에서, 즉 마이페이지에서 변경 시도
    """
    return service.user.change_password(req.state.auth.id, reset, req.state.backend)


@router.patch(path="/password/extend", name="비밀번호 연장")
@has_role(["USER"])
def extend_password(req: Request):
    return service.user.change_password(req.state.auth.id, None, req.state.backend)


@router.delete(path="", name="회원탈퇴", response_model=UserDefault)
@has_role(["USER"])
def leave(req: Request):
    return crud.user.remove(id=req.state.auth.id, session=req.state.backend)
    # return crud.user.update(update={}, session=req.state.backend)


@router.delete(path="/authenticate", name="로그아웃")
def deactivate(res: Response):
    res.set_cookie(key="access_token", max_age=0, secure=True, httponly=True, samesite="None")
    return True
