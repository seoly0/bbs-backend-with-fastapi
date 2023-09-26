from datetime import timedelta

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from core.entity import Board, BoardAud, BoardRequest, BoardRequestAud, Post
from core.model.board import BoardBest
from utils.timeUtils import get_now

from .base import CRUDBase


class BoardCURD(CRUDBase[Board, BoardAud]):
    def search(self, query: str, session: Session) -> list[Board]:
        return session.scalars(select(Board).where(Board.name.contains(query), Board.deleted == False)).all()

    def get_new_list(self, session: Session) -> list[Board]:
        return session.scalars(
            select(Board).where(Board.deleted == False).order_by(Board.created_at.desc()).limit(5)
        ).all()

    def get_best_list(self, session: Session) -> list[Board]:
        result = session.scalars(
            select(Board.id, Board.name, Board.parent_id, func.count("*").label("new_cnt"))
            .where(Board.deleted == False)
            .where(Post.deleted == False)
            .where(Post.created_at > get_now() - timedelta(days=1))
            .where(Post.board_id == Board.id)
            .group_by(Board.id)
            .order_by(desc("new_cnt"))
            .limit(5)
        ).all()

        more: list[Board] = []
        if len(result) < 5:
            more = session.scalars(
                select(Board).where(Board.id.not_in(list(map(lambda x: x.id, result)))).limit(5 - len(result))
            ).all()
        ret = result + more
        ret = list(
            map(
                lambda x: BoardBest(
                    id=x.id, name=x.name, parent_id=x.parent_id, new_cnt=x.new_cnt if hasattr(x, "new_cnt") else 0
                ),
                ret,
            )
        )
        return ret

    def test(self, session: Session):
        session.scalars(select(Board))
        pass


class BoardRequestCURD(CRUDBase[BoardRequest, BoardRequestAud]):
    pass


board = BoardCURD(Board, BoardAud)
board_request = BoardRequestCURD(BoardRequest, BoardRequestAud)
