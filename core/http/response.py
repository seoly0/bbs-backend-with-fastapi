import json

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class ResponseMessage:
    type: str
    level: str
    value: str

    def __init__(self, type, level, value):
        self.type = type
        self.level = level
        self.value = value


class ResponseModel:
    success: bool = None
    data: any = None
    error: any = None
    message: any = None

    def __init__(self, success, data: any, error: any = None, message: any = None):
        self.success = success
        self.data = data
        self.error = error
        self.message = message

    def dict(self):
        return jsonable_encoder(self)

    def dump(self):
        return json.dumps(self.dict())


class Response(JSONResponse):
    message = None
    error = None

    def __init__(
        self,
        content: any,
        status_code: int = 200,
        headers: dict | None = None,
        media_type: str | None = None,
        background: any = None,
        message: any = None,
        error: any = None,
        response_model: any = None,
    ) -> None:
        if response_model:
            if response_model.__config__.orm_mode:
                content = response_model.from_orm(content)
            else:
                content = response_model.parse_obj(content)
        self.message = message
        self.error = error
        super().__init__(content, status_code, headers, media_type, background)

    def render(self, content: any) -> bytes:
        return json.dumps(
            ResponseModel(
                success=True if self.error is None else False, data=content, message=self.message, error=self.error
            ).dict(),
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")
