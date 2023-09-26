from typing import Optional

from fastapi import APIRouter, Depends, UploadFile
from pydantic import EmailStr

from app import crud
from core.auth import has_role
from core.exception import MIMETypeException
from core.http.request import Page, Pagination, Request
from core.model.user import UserDefault, UserRoleCreate, UserWithRole
from libs.media import save
from settings import ENV

router = APIRouter()
router.tags = ["관리자 - 사용자"]
router.prefix = "/user"


@router.get(path="/by", name="사용자 찾기", response_model=UserWithRole)
@has_role(["CS"])
def get_user_by(request: Request, id: Optional[int] = None, email: Optional[EmailStr] = None):
    if id is not None:
        return crud.user.get(id, request.state.backend)
    elif email is not None:
        return crud.user.get_by_email(email, request.state.backend)
    else:
        raise Exception


@router.get(path="/list/page", name="사용자 목록", response_model=Pagination[UserDefault])
@has_role(["CS"])
def get_user_page(
    req: Request,
    page: Page = Depends(),
):
    return crud.user.get_page(page=page, session=req.state.backend)


@router.post(
    path="/role",
    name="권한 추가",
)
@has_role(["ADMIN"])
def create_user_role(req: Request, create: UserRoleCreate):
    return crud.user_role.create(create=create, session=req.state.backend)


# TODO
@router.patch(path="/password/reset", name="비밀번호 강제 초기화")
@has_role(["ADMIN"])
def reset_password(req: Request, id: int, password: str):
    """
    임시 비밀번호 발급
    """
    return id
    # return crud.user.update({'id': id, 'password': password}, session=req.state.backend)


# TODO
@router.patch(path="/password", name="비밀번호 강제 변경")
@has_role(["SUPER"])
def change_password(req: Request, id: int, password: str):
    """
    원하는 비밀번호로 설정
    """
    return id
    # return crud.user.update({'id': id, 'password': password}, session=req.state.backend)


@router.post(path="/thumbnail/default", name="사용자 기본 썸네일 설정")
@has_role(["CS"])
def set_default_user_thumbnail(req: Request, image: UploadFile):
    mime = image.content_type.split("/")[0]
    ext = image.content_type.split("/")[1]

    if mime != "image":
        raise MIMETypeException("이미지 형식의 파일이 아닙니다.")

    if ext not in ["png"]:
        raise MIMETypeException("PNG 형식만 업로드 해주세요.")

    path = ENV.MEDIA_USER_DEFAULT_THUMBNAIL  # 'thumbnail/user/default.png'
    save(path=path, file=image.file.fileno())

    return True
