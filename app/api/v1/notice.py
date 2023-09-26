from fastapi import APIRouter, Depends

from app import crud
from core.entity import Notice
from core.enum import NoticeState
from core.http.request import Page, Request

router = APIRouter()
router.tags = ["공지사항"]
router.prefix = "/notice"


@router.get("", name="공지사항 상세")
def serve_notice_detail_by_id(req: Request, id: int):
    return crud.notice.get(id=id, session=req.state.backend, check=("state", NoticeState.VISIBLE))


@router.get("/important/list", name="중요 공지사항 목록")
def serve_notice_important(req: Request):
    return crud.notice.get_important_list(req.state.backend)


@router.get("/list", name="공지사항 목록")
def serve_notice_list(req: Request, board_id: int | None = None):
    """
    - board_id가 0일시(파라미터 넘기지 않을 시) 전체 공지사항
    - board_id가 0이 아닐시 해당 게시판의 공지사항
    """
    return crud.notice.get_list(
        session=req.state.backend, limit=5, filter=(Notice.board_id == board_id, Notice.state == NoticeState.VISIBLE)
    )


@router.get("/list/page", name="공지사항 페이지")
def serve_notice_page(req: Request, page: Page = Depends()):
    return crud.notice.get_page(
        page=page, filter=(Notice.board_id == None, Notice.state == NoticeState.VISIBLE), session=req.state.backend
    )
