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

from .banned import router as banned_admin_router
from .board import router as board_admin_router
from .contact import router as contact_admin_router
from .faq import router as faq_admin_router
from .notice import router as notice_admin_router
from .scheduler import router as scheduler_admin_router
from .terms import router as terms_admin_router
from .user import router as user_admin_router

router = APIRouter()
router.include_router(user_admin_router)
router.include_router(terms_admin_router)
router.include_router(notice_admin_router)
router.include_router(faq_admin_router)
router.include_router(contact_admin_router)
router.include_router(board_admin_router)
router.include_router(banned_admin_router)
router.include_router(scheduler_admin_router)
api = FastAPI(
    debug=False,
    title="APIs for BBS",
    description="Bulletin Board System",
    version="2.0.0",
    contact={"name": ENV.APP_AUTHOR_NAME, "email": ENV.APP_AUTHOR_EMAIL},
    redoc_url=None,
    docs_url=None,
    openapi_url=f"/spec.json",
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
