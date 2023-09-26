from enum import Enum, auto


class StrEnum(str, Enum):
    """
    StrEnum is a Python ``enum.Enum`` that inherits from ``str``. The default
    ``auto()`` behavior uses the member name as its value.
    Example usage::
        class Example(StrEnum):
            UPPER_CASE = auto()
            lower_case = auto()
            MixedCase = auto()
        assert Example.UPPER_CASE == "UPPER_CASE"
        assert Example.lower_case == "lower_case"
        assert Example.MixedCase == "MixedCase"
    """

    def __new__(cls, value, *args, **kwargs):
        if not isinstance(value, (str, auto)):
            raise TypeError(f"Values of StrEnums must be strings: {value!r} is a {type(value)}")
        return super().__new__(cls, value, *args, **kwargs)

    def __str__(self):
        return str(self.value)

    def _generate_next_value_(name, *_):
        return name


class UserRoleType(StrEnum):
    USER = auto()
    CS = auto()
    ADMIN = auto()
    SUPER = auto()


class NoticeType(StrEnum):
    NORMAL = auto()
    IMPORTANT = auto()


class NoticeState(StrEnum):
    # ONBOARD = 'ONBOARD'
    # DEFAULT = 'DEFAULT'
    HIDDEN = auto()
    VISIBLE = auto()


class MailState(StrEnum):
    PENDING = auto()  # 대기중. 메일 최초 등록
    PROCESSING = auto()  # 처리중. 중복 발송을 방지
    COMPLETE = auto()  # 완료.
    FAIL = auto()  # 실패.


class CertState(StrEnum):
    PENDING = auto()  # 인증 대기
    COMPLETE = auto()  # 인증이 강제 취소되었음 (ex. 재발급)
    CANCELED = auto()  # 인증이 정상 종료되었음
    # EXPIRED = auto()  # expire 타임을 측정하는데 의미가 있을지?


class CertType(StrEnum):
    USER_JOIN = auto()
    USER_PWRESET = auto()


class State(StrEnum):
    PENDING = auto()
    ACTIVE = auto()
    BLOCKED = auto()


class UserState(StrEnum):
    PENDING = auto()  # 최신 약관 미동의 상태
    ACTIVE = auto()  # 활성 상태
    ACCUSED = auto()  # 사용자에 의한 신고 XX회 누적 상태 (관리자 확인)
    BLOCKED = auto()  # 관리자에 의한 직권 차단 상태 (XX일 글/댓글 작성 불가)
    SLEEP = auto()  # 휴면 상태


class PostState(StrEnum):
    ACTIVE = auto()  # 활성상태
    ACCUSED = auto()  # 사용자에 의한 신고 XX회 누적 상태 (사용자에게 경고)
    FROZEN = auto()  # 관리자에 의한 차단 상태 (사용자 게시글 수정 및 댓글 작성 불가)
    BLOCKED = auto()  # 관리자에 의한 직권 차단 상태 (게시글이 노출되지 않음)


class ReplyState(StrEnum):
    ACTIVE = auto()  # 활성상태
    ACCUSED = auto()  # 사용자에 의한 신고 XX회 누적 상태 (블라인드)


class BoardState(StrEnum):
    ACTIVE = auto()  # 활성상태
    FROZEN = auto()  # 관리자에 의한 차단 상태 (사용자 게시글 작성 불가)
    BLOCKED = auto()  # 관리자에 의한 차단 상태 (사용자 접근불가)


class BoardRequestState(StrEnum):
    PENDING = auto()
    ACCEPTED = auto()
    REJECTED = auto()


class ContactState(StrEnum):
    PENDING = auto()
    PROCESS = auto()
    COMPLETE = auto()


class RequestActionType(StrEnum):
    ACCEPT = auto()
    REJECT = auto()
