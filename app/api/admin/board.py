from fastapi import APIRouter

from app import crud
from core.entity.table_board_request import BoardRequest
from core.enum import BoardRequestState, RequestActionType
from core.http.request import Request
from core.model.board import BoardAcceptCreate, BoardCreate, BoardUpdate

router = APIRouter()
router.tags = ["관리자 - 게시판"]
router.prefix = "/board"


@router.get("/create/request")
def get_request_list(req: Request):
    return crud.board_request.get_list(
        session=req.state.backend, filter=(BoardRequest.state == BoardRequestState.PENDING)
    )


@router.put("/create/request/{id}")
def accept_request(req: Request, id: int, action: RequestActionType, data: BoardAcceptCreate):
    obj = crud.board_request.get(id, session=req.state.backend)

    if action == RequestActionType.ACCEPT:
        obj.state = BoardRequestState.ACCEPTED
        crud.board_request.update(obj, session=req.state.backend)
    elif action == RequestActionType.REJECT:
        obj.state = BoardRequestState.REJECTED
    else:
        pass

    return True


@router.post("")
def create_board(req: Request, create: BoardCreate):
    create.parent_id = create.parent_id if create.parent_id else None
    return crud.board.create(create, req.state.backend)


@router.put("")
def update_board(req: Request, update: BoardUpdate):
    update.parent_id = update.parent_id if update.parent_id else None
    return crud.board.update(update, req.state.backend)


@router.patch("/state")
def toggle_board_state(req: Request):
    return True
