from fastapi import APIRouter

from app import crud
from core.auth import has_role
from core.http.request import Request
from core.model.faq import FAQCreate, FAQUpdate, FAQUpdateShow

router = APIRouter()
router.tags = ["관리자 - FAQ"]
router.prefix = "/faq"


@router.get("/list", name="FAQ 목록")
@has_role(["CS"])
def serve_faq_list(request: Request):
    return crud.faq.get_list(session=request.state.backend)


@router.post("", name="FAQ 등록")
@has_role(["CS"])
def post_faq(request: Request, create: FAQCreate):
    return crud.faq.create(create=create, session=request.state.backend)


@router.put("", name="FAQ 수정")
@has_role(["CS"])
def update_faq(request: Request, update: FAQUpdate):
    return crud.faq.update(update=update, session=request.state.backend)


@router.patch("/show", name="FAQ 노출 설정")
@has_role(["CS"])
def toggle_show_faq(request: Request, update: FAQUpdateShow):
    return crud.faq.update(update=update, session=request.state.backend)


@router.delete("", name="FAQ 삭제")
@has_role(["CS"])
def remove_faq(request: Request, id: int):
    crud.faq.remove(id, request.state.backend)
    return True
