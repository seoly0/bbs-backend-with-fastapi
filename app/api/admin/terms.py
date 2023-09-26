from fastapi import APIRouter

from app import crud
from core.http.request import Request
from core.model.terms import TermsCreate, TermsUpdate

router = APIRouter()
router.tags = ["관리자 - 약관"]
router.prefix = "/terms"


@router.post("")
def create_terms(req: Request, create: TermsCreate):
    return crud.terms.create(create=create, session=req.state.backend)


@router.put("")
def update_terms(req: Request, update: TermsUpdate):
    return crud.terms.update(update=update, session=req.state.backend)
