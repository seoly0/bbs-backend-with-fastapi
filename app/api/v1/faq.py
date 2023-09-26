from fastapi import APIRouter

from app import crud
from core.http.request import Request

router = APIRouter()
router.tags = ["FAQ"]
router.prefix = "/faq"


@router.get("/list/all", name="FAQ 목록")
def serve_faq_list(request: Request):
    return crud.faq.get_visible_list(request.state.backend)
