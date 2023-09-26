from fastapi import APIRouter

from app import crud
from core.http.request import Request

router = APIRouter()
router.tags = ["약관"]
router.prefix = "/terms"


@router.get(path="/service", name="이용약관")
async def serve_service_policy(req: Request):
    return crud.terms.get_service(req.state.backend)


@router.get(path="/privacy", name="개인정보처리방침")
async def serve_privacy_policy(req: Request):
    return crud.terms.get_privacy(req.state.backend)
