from datetime import datetime, timedelta
from functools import wraps

from fastapi import Request
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from starlette.middleware.base import BaseHTTPMiddleware  # noqa

from core.exception import (
    ExpiredAuthenticationException,
    InvalidAuthenticationException,
    NoAuthenticationException,
    NotAuthorizedException,
)
from settings import ENV


class Authentication:
    id: int
    email: str
    roles: list[str]
    extra: dict[str, any]

    def __init__(self, id, email, roles, extra=None):
        self.id = id
        self.email = email
        self.roles = roles
        self.extra = extra


class AuthenticationInjectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        credentials = request.cookies.get("access_token")
        if credentials:
            try:
                token = decode(jwt=credentials, key=ENV.JWT_SECRET, algorithms=[ENV.JWT_ALGORITHM])
                auth = Authentication(id=token["id"], email=token["email"], roles=token["roles"], extra=token["extra"])
                request.state.auth = auth
            except:
                request.state.auth = None
        else:
            request.state.auth = None
        return await call_next(request)


def issue(auth: Authentication):
    expire = datetime.utcnow() + timedelta(minutes=ENV.JWT_EXPIRE)

    payload = auth.__dict__
    payload.update({"exp": expire})
    token = encode(
        payload=payload,
        key=ENV.JWT_SECRET,
        algorithm=ENV.JWT_ALGORITHM,
    )
    # HTTPAuthorizationCredentials(scheme='Bearer', credentials=token)
    return token


def has_role(roles: list[str] = []):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for arg in kwargs:
                if isinstance(kwargs[arg], Request):
                    # print(kwargs[arg].state.auth)
                    if not kwargs[arg].state.auth:
                        # 로그아웃
                        raise NotAuthorizedException

                    for role in roles:
                        if "SUPER" in kwargs[arg].state.auth.roles:
                            break
                        elif role not in kwargs[arg].state.auth.roles:
                            # 롤 없음
                            raise NotAuthorizedException

            return func(*args, **kwargs)

        return wrapper

    return inner


# class CheckAuthentication:
#     async def __call__(self, req: Request) -> Optional[Authentication]:
#         try:
#             credentials = req.cookies.get('access_token')
#             token = decode(
#                 jwt=credentials,
#                 key=CONFIG.JWT.secret,
#                 algorithms=[CONFIG.JWT.algorithm]
#             )
#             auth = Authentication(
#                 id=token['id'],
#                 email=token['email'],
#                 roles=token['roles'],
#                 extra=token['extra']
#             )
#         except DecodeError:
#             return
#         except ExpiredSignatureError:
#             return
#         except Exception:
#             return

#         return auth


# class RequireAuthentication:
#     async def __call__(self, req: Request) -> Optional[Authentication]:
#         try:
#             credentials = req.cookies.get('access_token')
#             token = decode(
#                 jwt=credentials,
#                 key=CONFIG.JWT.secret,
#                 algorithms=[CONFIG.JWT.algorithm]
#             )
#             auth = Authentication(
#                 id=token['id'],
#                 email=token['email'],
#                 roles=token['roles'],
#                 extra=token['extra']
#             )
#         except DecodeError:
#             raise InvalidAuthenticationException
#         except ExpiredSignatureError:
#             raise ExpiredAuthenticationException
#         except Exception:
#             raise NoAuthenticationException

#         return auth


# def has_role(roles: list[str], exception=None):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(request):
#             if request.state.auth:
#                 user_roles = request.state.auth.roles
#                 for role in roles:
#                     if role not in user_roles:
#                         raise NotAuthorizedException
#                     else:
#                         continue
#             else:
#                 raise NotAuthorizedException

#             return func(request)
#         return wrapper
#     return decorator

# def has_role(roles: list[str]):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(request, *args, **kwargs):
#             for key in kwargs:
#                 value = kwargs[key]
#                 if isinstance(value, Authentication):
#                     for role in roles:
#                         if role not in value.roles:
#                             raise NotAuthorizedException
#                 else:
#                     continue
#                     # raise NotAuthorizedException

#             # result = None
#             # try:
#             #     result = await func(request, *args, **kwargs)
#             # except Exception as e:
#             #     pass
#             print(request.state.backend)
#             return func(request, *args, **kwargs)
#         return wrapper
#     return decorator
