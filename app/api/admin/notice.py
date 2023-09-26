from fastapi import APIRouter, Depends

from app import crud
from core.auth import has_role
from core.http.request import Page, Request
from core.model.notice import NoticeCreate, NoticeToggleVisible, NoticeUpdate

router = APIRouter()
router.tags = ["관리자 - 공지사항"]
router.prefix = "/notice"


@router.get("")
@has_role(["CS"])
def get_notice(req: Request, id: int):
    return crud.notice.get(id=id, session=req.state.backend)


@router.get("/list/page")
@has_role(["CS"])
def get_notice_page(req: Request, page: Page = Depends()):
    return crud.notice.get_page(page=page, session=req.state.backend)


@router.post("")
@has_role(["CS"])
def post_notice(req: Request, create: NoticeCreate):
    create.writer_id = req.state.auth.id
    create.writer_nick = req.state.auth.extra["nick"]
    create.board_id = create.board_id if create.board_id else None
    return crud.notice.create(create, session=req.state.backend)


@router.put("")
@has_role(["CS"])
def update_notice(req: Request, update: NoticeUpdate):
    return crud.notice.update(update, session=req.state.backend)


@router.patch("")
@has_role(["CS"])
def toggle_visible(req: Request, update: NoticeToggleVisible):
    return crud.notice.update(update, session=req.state.backend)
