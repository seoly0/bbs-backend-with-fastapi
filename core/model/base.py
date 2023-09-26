from pydantic import BaseModel

from settings import ENV
from utils.pathUtils import HttpURL


class Base(BaseModel):
    pass

    class Config:
        json_encoders = {
            # datetime: lambda v: v.replace(tzinfo=UTC).astimezone(KST).strftime('%Y-%m-%d %H:%M:%S %Z')
        }


def media_url_composite(v: str) -> str:
    return (HttpURL(ENV.MEDIA_HOST) / (v if v else ENV.MEDIA_USER_DEFAULT_THUMBNAIL)).toString()
