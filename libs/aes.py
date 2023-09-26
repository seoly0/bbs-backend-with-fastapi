import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from settings import ENV

BS = 16  # padding
KEY: str = ENV.AES_SECRET


def encrypt(plain: str) -> str:
    raw = pad(plain.encode("utf-8"), BS)
    cipher = AES.new(
        key=pad(KEY.encode("utf-8"), BS),
        iv=pad(KEY.encode("utf-8"), BS),
        mode=AES.MODE_CBC,
    )
    return base64.b64encode(cipher.encrypt(raw)).decode("utf-8")


def decrypt(code: str) -> str:
    enc = base64.b64decode(code.encode("utf-8"))
    cipher = AES.new(
        key=pad(KEY.encode("utf-8"), BS),
        iv=pad(KEY.encode("utf-8"), BS),
        mode=AES.MODE_CBC,
    )
    return unpad(cipher.decrypt(enc), BS).decode("utf-8")
