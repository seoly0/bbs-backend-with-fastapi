from fastapi import Request, status
from fastapi.exceptions import StarletteHTTPException

from core.http.response import JSONResponse, ResponseMessage, ResponseModel


class ExceptionModel(Exception):
    status: int
    code: str
    message: str
    message_print: bool = True
    message_type = ""
    message_level = ""

    def __init__(self, message=None, message_type="ALERT", message_level="ERROR", message_print=True):
        if message:
            self.message = message
        if message_print:
            self.message_print = message_print
        if message_type:
            self.message_type = message_type
        if message_level:
            self.message_level = message_level
        super().__init__()


async def http_404_handler(request: Request, exception: StarletteHTTPException):
    if exception.status_code == 404:
        pass
    return JSONResponse({}, 404)


# deprecated
# async def default_exception_handler(request: Request, exception: Exception):
#     logger.error(request, exception)
#     return JSONResponse(
#         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         content=ResponseModel(
#             success=False,
#             data=None,
#             error='XXXX',
#             message=ResponseMessage(
#                 type='ALERT',
#                 level='ERROR',
#                 msg='내부 오류 발생'
#             )
#         ).dict()
#     )


async def custom_exception_handler(request: Request, exception: ExceptionModel):
    return JSONResponse(
        status_code=exception.status,
        content=ResponseModel(
            success=False,
            data=None,
            error=exception.code,
            message=ResponseMessage(type=exception.message_type, level=exception.message_level, value=exception.message)
            if exception.message_print
            else None,
        ).dict(),
    )


class InternalServerException(ExceptionModel):
    status = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = ""
    message = "서버 오류입니다."


class TestException(ExceptionModel):
    status = status.HTTP_400_BAD_REQUEST
    code = "TEST"
    message = "This is test Exception."


class ResponseNoneException(ExceptionModel):
    status = status.HTTP_400_BAD_REQUEST
    code = ""
    message = "데이터가 존재하지 않습니다."


class UserRegisterFailException(ExceptionModel):
    status = status.HTTP_400_BAD_REQUEST
    code = ""
    message = "회원가입에 실패했습니다."


class AuthenticationFailException(ExceptionModel):
    status = status.HTTP_400_BAD_REQUEST
    code = ""
    message = "사용자가 없거나 잘못된 암호입니다."


class InvalidInputException(ExceptionModel):
    status = status.HTTP_400_BAD_REQUEST
    code = ""
    message = "잘못된 입력입니다."


class NoAuthenticationException(ExceptionModel):
    status = status.HTTP_401_UNAUTHORIZED
    code = ""
    message = "인증정보가 없습니다."


class ExpiredAuthenticationException(ExceptionModel):
    status = status.HTTP_401_UNAUTHORIZED
    code = ""
    message = "인증정보가 만료되었습니다."


class InvalidAuthenticationException(ExceptionModel):
    status = status.HTTP_401_UNAUTHORIZED
    code = ""
    message = "유효하지 않은 인증정보입니다."


class NotAuthorizedException(ExceptionModel):
    status = status.HTTP_403_FORBIDDEN
    code = ""
    message = "권한이 없습니다."


class EntityNotActivatedException(ExceptionModel):
    status = status.HTTP_422_UNPROCESSABLE_ENTITY
    code = ""
    message = "사용할 수 없는 데이터입니다."


class EntityNotExistException(ExceptionModel):
    status = status.HTTP_404_NOT_FOUND
    code = ""
    message = "존재하지 않는 데이터입니다."


class EntityNotAuthorizedException(ExceptionModel):
    status = status.HTTP_401_UNAUTHORIZED
    code = ""
    message = "권한이 없습니다."


class SFTPConnectionException(ExceptionModel):
    status = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = ""
    message = "업로드에 실패했습니다."


class MIMETypeException(ExceptionModel):
    status = status.HTTP_400_BAD_REQUEST
    code = ""
    message = "잘못된 형식의 파일입니다."


class SearchTooShortException(ExceptionModel):
    status = status.HTTP_400_BAD_REQUEST
    code = ""
    message = "검색어가 너무 짧습니다."


class BannedWordException(ExceptionModel):
    status = status.HTTP_400_BAD_REQUEST
    code = ""
    message = "금지된 단어를 사용했습니다."
