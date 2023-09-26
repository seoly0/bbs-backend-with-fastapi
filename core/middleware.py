# https://fastapi.tiangolo.com/advanced/middleware/
# https://www.starlette.io/middleware/

import time
import traceback
from http.client import responses
from logging import getLogger

import sqltap
from fastapi.middleware.cors import CORSMiddleware  # noqa
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware  # noqa
from uvicorn.protocols.utils import get_path_with_query_string

from app import crud
from core.backend.postgres import SessionProvider
from core.entity import UserAccess
from core.exception import InternalServerException
from core.http.request import Request
from core.http.response import Response, ResponseMessage
from settings import ENV
from utils.dateUtils import midnight, server_now

cors_options = {
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    "allow_headers": ["*"],
    "allow_origins": ENV.CORS_ALLOW_ORIGINS.split(","),
}

color = {
    2: "32m",
    3: "36m",
    4: "31m",
    5: "31m",
}


class QueryLoggingMiddleware(BaseHTTPMiddleware):
    logger = getLogger("data")

    async def dispatch(self, request: Request, call_next):
        profiler = sqltap.start()
        start = time.process_time()
        response = await call_next(request)
        end = time.process_time()
        statistics = profiler.collect()
        for statistic in statistics:
            query = f"""{str(statistic.text)}\nparams: {statistic.params}"""
            self.logger.debug(f"""\033[90m\n{query}\nexecuted in {((end - start) * 1000):.2f}ms\033[0m""")
        return response


class RequestLoggingkMiddleware(BaseHTTPMiddleware):
    logger = getLogger("app.Request")

    async def dispatch(self, request: Request, call_next):
        scope = request.scope
        host = request.client.host
        path = get_path_with_query_string(scope)
        http_type = f"""{scope.get('scheme').upper()}/{scope.get('http_version')}"""
        method = request.method
        msg = f"""{host} - \033[1m{method} {path} {http_type}\033[0m"""
        self.logger.info(msg)
        start = time.process_time()
        response = await call_next(request)
        end = time.process_time()
        code = response.status_code
        msg = f"""{host} - responded in \033[1m{((end - start) * 1000):.2f}ms\033[0m"""
        msg += f""" / \033[{color[int(code / 100)]}{code} {responses[code]}\033[0m"""
        self.logger.info(msg)
        return response


class UserAccessRecordMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        session = SessionProvider()
        user = request.state.auth
        host = request.client.host
        device = request.headers["user-agent"]
        if user:
            access = crud.user_access.get_list(
                filter=(
                    UserAccess.user_id == user.id,
                    UserAccess.ip == host,
                    UserAccess.device == device,
                    UserAccess.when >= midnight(),
                ),
                session=session,
            )
            if len(access) == 0:
                crud.user_access.create(
                    {
                        "user_id": user.id,
                        "ip": host,
                        "when": server_now(),
                        "device": device,
                        "where": "",
                    },
                    session=session,
                )
                session.commit()
            session.close()
        return await call_next(request)


class LocaleCheckMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # print(request.headers.get('accept-language'))
        return await call_next(request)


class InternalServerErrorHandleMiddleware(BaseHTTPMiddleware):
    logger = getLogger("error.internal")

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)

        except Exception:
            self.logger.error(traceback.format_exc())
            return Response(
                status_code=500,
                content=None,
                error=InternalServerException.code,
                message=ResponseMessage(type="ALERT", level="ERROR", value=InternalServerException.message),
            )


class DatabaseSessionInjectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.backend = SessionProvider()
        response = None

        try:
            response = await call_next(request)
            request.state.backend.commit()

        except Exception as e:
            request.state.backend.rollback()

        finally:
            request.state.backend.close()

        return response
