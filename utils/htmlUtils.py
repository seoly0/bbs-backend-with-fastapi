from html2text import HTML2Text
from lxml.html.clean import Cleaner


def get_clean(origin: str) -> str:
    """
    스크립트/스타일 태그 제거
    """
    cleaner = Cleaner()
    cleaner.style = True
    cleaner.javascript = True

    return cleaner.clean_html(origin)


def get_plain(origin: str) -> str:
    """
    검색용 데이터 (HTML -> Plain Text) 생성
    """

    h = HTML2Text()
    # h.escape_snob = False
    h.body_width = 0
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_emphasis = True
    plain = h.handle(origin).replace("\n", " ").strip()

    return plain
