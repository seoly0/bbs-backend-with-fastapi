import datetime
from io import BytesIO, FileIO
from uuid import uuid4

from fastapi import APIRouter, Request, UploadFile
from PIL import Image

from core.auth import has_role
from core.exception import MIMETypeException
from libs.media import save

router = APIRouter()
router.tags = ["미디어"]
router.prefix = "/media"


@router.post(
    path="/upload",
    name="이미지 업로드",
)
@has_role(["USER"])
def image_upload(req: Request, image: UploadFile):
    mime = image.content_type.split("/")[0]
    ext = image.content_type.split("/")[1]

    if mime != "image":
        raise MIMETypeException("이미지 형식의 파일이 아닙니다.")

    # buf = BytesIO(image.file)

    # image = Image.open(image.file)

    # print(image.)

    return save(
        path=f"upload/{datetime.date.today()}_{req.state.auth.id}_{uuid4()}.{ext}",
        file=image.file.fileno(),
        content_type=image.content_type,
    )
