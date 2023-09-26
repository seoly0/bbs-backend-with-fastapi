from fastapi import APIRouter

from app import crud
from core.auth import has_role
from core.entity import Board
from core.http.request import Request
from core.model.board import BoardBest, BoardRequestCreate

router = APIRouter()
router.tags = ["게시판"]
router.prefix = "/board"


@router.get(path="/search", name="게시판 검색")
def serve_board_search(req: Request, query: str):
    return crud.board.search(query, req.state.backend)


@router.get(path="/best/list", name="인기 게시판 목록", response_model=list[BoardBest])
def serve_best_board_list(req: Request):
    """
    조회 시점으로부터 지난 24시간동안 가장 글 작성수가 많았던 상위 5개 게시판 목록
    """
    result = crud.board.get_best_list(req.state.backend)
    cnt = len(result)
    return result


@router.get(path="/new/list", name="신규 게시판 목록")
def serve_new_board_list(req: Request):
    return crud.board.get_new_list(req.state.backend)


@router.get("")
def serve_board(req: Request, id: int):
    return crud.board.get(id=id, session=req.state.backend)


@router.get(path="/list", name="전체 게시판 목록")
def serve_board_list(req: Request):
    return crud.board.get_list(session=req.state.backend)


@router.get(path="/main/list", name="1뎁스 게시판 목록")
def serve_main_board_list(req: Request):
    return crud.board.get_list(session=req.state.backend, filter=Board.parent_id == 0)


@router.get(path="/sub/list", name="2뎁스 게시판 목록")
def serve_sub_board_list(req: Request, parent_id: int):
    return crud.board.get_list(session=req.state.backend, filter=Board.parent_id == parent_id)


@router.post(path="/request/create", name="게시판 생성 요청")
@has_role(["USER"])
def request_create(req: Request, create: BoardRequestCreate):
    create.user_id = req.state.auth.id
    create.user_nick = req.state.auth.extra.get("nick")
    return crud.board_request.create(create, req.state.backend)
