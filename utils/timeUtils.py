from datetime import datetime

from pytz import timezone

UTC = timezone("UTC")
KST = timezone("Asia/Seoul")
TIME_FORMAT = "%Y-%m-%d %H:%M:%S %Z"


def get_now():
    return datetime.now().replace(tzinfo=UTC)
