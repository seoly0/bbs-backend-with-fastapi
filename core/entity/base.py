from pytz import timezone
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import declarative_base, declared_attr

from utils.strUtils import snake_case

# from sqlalchemy.types import TypeDecorator


UTC = timezone("UTC")
KST = timezone("Asia/Seoul")
TIME_FORMAT = "%Y-%m-%d %H:%M:%S %Z"


# class DateTimeUTC(TypeDecorator):
#     impl = DateTime
#     cache_ok = True

#     def __repr__(self):
#         return "DateTime(timezone=True)"

#     def process_bind_param(self, value, dialect):
#         return value

#     def process_result_value(self, value: datetime, dialect):
#         # .strftime(TIME_FORMAT)
#         return value.replace(tzinfo=UTC).astimezone(KST) if value else value


Entity = declarative_base(class_registry={})


class BaseMixin:
    id = Column(Integer, primary_key=True, index=True)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __name__: str
    __allow_unmapped__ = True

    @declared_attr
    def __tablename__(self) -> str:
        return snake_case(self.__name__)


class AuditMixin:
    aid = Column(Integer, primary_key=True)
    id = Column(Integer)
    deleted = Column(Boolean)
    created_by = Column(Integer)
    created_at = Column(String)
    updated_by = Column(Integer)
    updated_at = Column(String)

    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        return snake_case(self.__name__)
