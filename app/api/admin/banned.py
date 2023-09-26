from fastapi import APIRouter

from app.batch.banning.tasks import invoke_build
from app.crud import banned_word
from core.auth import has_role
from core.http.request import Request

router = APIRouter()
router.tags = ["관리자 - 금칙어"]
router.prefix = "/banned"


@router.get("")
def get_list(req: Request):
    data = banned_word.get_list(session=req.state.backend)
    return data


@router.get("/build")
@has_role(["SUPER"])
def get_list_with_build(req: Request):
    invoke_build.delay()
    return True


@router.post("")
@has_role(["SUPER"])
def insert(req: Request, word: str):
    banned_word.create(create={"word": word}, session=req.state.backend)
    return word


@router.delete("")
@has_role(["SUPER"])
def delete(req: Request, id: int):
    banned_word.remove(id=id, session=req.state.backend)
