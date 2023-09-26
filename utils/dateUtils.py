from datetime import date, datetime

import pytz

UTC = pytz.UTC
KST = pytz.timezone("Asia/Seoul")
TIME_FORMAT = "%Y-%m-%d %H:%M:%S %Z"


def server_now() -> datetime:
    return datetime.now(tz=UTC)


def midnight() -> datetime:
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).astimezone(KST)


def dday(target: date | datetime):
    if type(target) == datetime:
        if not target.tzinfo:
            target = target.replace(tzinfo=KST)
        now = server_now()
        return (now - target).days

    elif type(target) == date:
        today = date.today()
        return (today - target).days
    else:
        raise TypeError("only allowed date or datetime")
