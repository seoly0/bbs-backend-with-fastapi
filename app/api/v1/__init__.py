from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import APIRouter, FastAPI

from core.auth import AuthenticationInjectMiddleware
from core.exception import (ExceptionModel, StarletteHTTPException,
                            custom_exception_handler, http_404_handler)
from core.http.response import Response
from core.middleware import (CORSMiddleware, DatabaseSessionInjectMiddleware,
                             InternalServerErrorHandleMiddleware,
                             LocaleCheckMiddleware, QueryLoggingMiddleware,
                             RequestLoggingkMiddleware, cors_options)
from settings import ENV

from .board import router as board_router
from .cert import router as cert_router
from .common import router as common_router
from .contact import router as contact_router
from .faq import router as faq_router
from .media import router as media_router
from .notice import router as notice_router
from .post import router as post_router
from .terms import router as terms_router
from .thumbs import router as thumbs_router
from .user import router as user_router

VERSION = "1.9.0"

router = APIRouter()
router.include_router(common_router)
router.include_router(media_router)
router.include_router(cert_router)
router.include_router(terms_router)
router.include_router(notice_router)
router.include_router(user_router)
router.include_router(faq_router)
router.include_router(contact_router)
router.include_router(board_router)
router.include_router(post_router)
router.include_router(thumbs_router)


api = FastAPI(
    debug=False,
    title="APIs for BBS",
    description="Bulletin Board System",
    version=VERSION,
    contact={"name": ENV.APP_AUTHOR_NAME, "email": ENV.APP_AUTHOR_EMAIL},
    redoc_url=None,
    openapi_url=f"/spec.json",
    docs_url="/spec-ui",
    routes=router.routes,
    default_response_class=Response,
)

# Add Middleware
# 가장 나중
api.add_middleware(CORSMiddleware, **cors_options)
api.add_middleware(InternalServerErrorHandleMiddleware)
api.add_middleware(AuthenticationInjectMiddleware)
api.add_middleware(DatabaseSessionInjectMiddleware)
api.add_middleware(LocaleCheckMiddleware)
api.add_middleware(QueryLoggingMiddleware)
api.add_middleware(RequestLoggingkMiddleware)
api.add_middleware(CorrelationIdMiddleware)  # request id 생성
# 가장 먼저

# # Add Error Handler
api.add_exception_handler(ExceptionModel, custom_exception_handler)
api.add_exception_handler(StarletteHTTPException, http_404_handler)
