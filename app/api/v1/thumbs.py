from fastapi import APIRouter

from app import service
from core.auth import has_role
from core.http.request import Request
from core.model.thumb import ThumbDefault

router = APIRouter()
router.tags = ["따봉"]
router.prefix = "/thumbs"


@router.post(path="", name="따봉 누르기")
@has_role(["USER"])
def reflect(
    req: Request,
    thumb: ThumbDefault,
):
    return service.thumb.reflect(thumb=thumb, uid=req.state.auth.id, session=req.state.backend)
