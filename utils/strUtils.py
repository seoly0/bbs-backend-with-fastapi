import random
import re
import string


def snake_case(s):
    return "_".join(re.sub("([A-Z][a-z]+)", r" \1", re.sub("([A-Z]+)", r" \1", s.replace("-", " "))).split()).lower()


def to_int(
    val: str,
) -> int | str:
    try:
        return int(val)
    except ValueError:
        return val


def to_bool(bal: str) -> bool | str:
    pass


def random_string(length=6):
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
