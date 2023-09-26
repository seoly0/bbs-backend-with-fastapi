from fastapi import APIRouter

from app import crud
from core.auth import has_role
from core.entity import Contact
from core.http.request import Request
from core.model.contact import ContactCreate, ContactUpdate

router = APIRouter()
router.tags = ["1:1 문의"]
router.prefix = "/contact"


@router.get(path="", name="1:1 문의 보기")
@has_role(["USER"])
def serve_contact(req: Request, id: int):
    return crud.contact.get(id=id, session=req.state.backend, check=("user_id", req.state.auth.id))


@router.post("", name="1:1 문의 생성")
@has_role(["USER"])
def create_contact(req: Request, create: ContactCreate):
    create.user_id = req.state.auth.id
    return crud.contact.create(create, req.state.backend)


@router.put("", name="1:1 문의 수정")
@has_role(["USER"])
def update_contact(req: Request, update: ContactUpdate):
    return crud.contact.update(update=update, session=req.state.backend, check=("user_id", req.state.auth.id))


@router.delete(path="", name="1:1 문의 삭제")
@has_role(["USER"])
def delete_contact(req: Request, id: int):
    return crud.contact.remove(id=id, session=req.state.backend, check=("user_id", req.state.auth.id))


@router.get(path="/list", name="사용자별 1:1 문의 목록")
@has_role(["USER"])
def serve_contact_list(req: Request):
    return crud.contact.get_list(session=req.state.backend, filter=Contact.user_id == req.state.auth.id)


@router.get("/category/list", name="1:1 문의 항목 목록")
def serve_category_list(request: Request):
    return crud.contact_category.get_list(session=request.state.backend)
