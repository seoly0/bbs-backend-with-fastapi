from .base import Base


class BoardCreate(Base):
    name: str
    parent_id: int | None = None


class BoardUpdate(BoardCreate):
    id: int


class BoardDefault(BoardUpdate):
    class Config:
        orm_mode = True


class BoardRequestCreate(Base):
    name: str
    reason: str
    parent_id: int | None
    user_id: int
    user_nick: str


class BoardAcceptCreate(Base):
    name: str | None
    parent_id: int | None


class BoardBest(Base):
    id: int
    name: str
    parent_id: int | None
    new_cnt: int
