from logging import getLogger

from fastapi import APIRouter
from sqlalchemy.orm import Session

from core.backend.postgres import SessionProvider
from libs.aes import decrypt, encrypt
from libs.geographic import get_position_by_ip_address
from utils.strUtils import random_string

router = APIRouter()
router.tags = ["일반"]
router.prefix = "/common"

logger = getLogger(__name__)


@router.get("/check/service")
async def check_service():
    return True


@router.get("/check/db")
async def check_db():
    session: Session = SessionProvider()
    session.execute("SELECT * FROM user").first()
    session.close()
    return True


@router.get("/check/redis")
async def check_redis():
    return True


@router.get("/rand/str")
def rand_str(length: int | None = None):
    return random_string(6 if length is None else length)


@router.get("/aes/encrypt")
def aes_encrypt(plain: str):
    return encrypt(plain)


@router.get("/aes/decrypt")
def aes_encrypt(code: str):
    return decrypt(code)


@router.get("/geographic/ip")
def get_position(ip: str):
    return get_position_by_ip_address(ip)

