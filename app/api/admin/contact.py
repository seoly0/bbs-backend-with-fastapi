from fastapi import APIRouter, Depends

from app import crud
from core.auth import has_role
from core.entity import Contact
from core.enum import ContactState
from core.http.request import Request
from core.model.contact import (ContactAnswer, ContactCategoryCreate,
                                ContactCategoryUpdate, ContactUpdateState)
from core.model.filter import Page

router = APIRouter()
router.tags = ["관리자 - 1:1 문의"]
router.prefix = "/contact"


@router.get("")
@has_role(["CS"])
def get_contact(req: Request, id: int):
    return crud.contact.get(id=id, session=req.state.backend)


@router.get("/list/page")
@has_role(["CS"])
def get_contact_list_paged(req: Request, page: Page = Depends()):
    return crud.contact.get_page(page=page, session=req.state.backend)


# TODO 아래 세 함수는 위 함수에 통합 + 추가 필터(작성자별, 답변자별)
@router.get("/pending/list/page")
@has_role(["CS"])
def get_contact_list_pending_paged(req: Request, page: Page = Depends()):
    return crud.contact.get_page(
        page=page,
        filter=(Contact.state == ContactState.PENDING),
        session=req.state.backend,
    )


@router.get("/process/list/page")
@has_role(["CS"])
def get_contact_list_process_paged(req: Request, page: Page = Depends()):
    return crud.contact.get_page(
        page=page,
        filter=(Contact.state == ContactState.PROCESS),
        session=req.state.backend,
    )


@router.get("/complete/list/page")
@has_role(["CS"])
def get_contact_list_complete_paged(req: Request, page: Page = Depends()):
    return crud.contact.get_page(
        page=page,
        filter=(Contact.state == ContactState.COMPLETE),
        session=req.state.backend,
    )


@router.post("/answer")
@has_role(["CS"])
def answer_contact(req: Request, answer: ContactAnswer):
    answer.cs_id = req.state.auth.id
    answer.cs_nick = req.state.auth.extra.get("nick")
    return crud.contact.update(update=answer, session=req.state.backend)


@router.patch("/answer")
@has_role(["CS"])
def change_state_contact(req: Request, update: ContactUpdateState):
    return crud.contact.update(update=update, session=req.state.backend)


@router.post("/category", name="1:1문의 항목 생성")
@has_role(["ADMIN"])
def create_category(request: Request, create: ContactCategoryCreate):
    return crud.contact_category.create(create, request.state.backend)


@router.put("/category", name="1:1문의 항목 수정")
@has_role(["ADMIN"])
def update_category(request: Request, update: ContactCategoryUpdate):
    return crud.contact_category.update(update, request.state.backend)


@router.delete("/category", name="1:1문의 항목 삭제")
@has_role(["ADMIN"])
def remove_category(request: Request, id: int):
    return crud.contact_category.remove(id, request.state.backend)


# @router.post("/test", name="1:1문의 항목 생성")
# def create_category(request: Request, name: str = Form()):
#     create = ContactCategoryCreate(name=name)
#     return crud.contact_category.create(create, request.state.backend)
