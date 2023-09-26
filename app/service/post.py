from sqlalchemy.orm import Session

from app import crud
from app.batch.banning.methods import validate
from core.enum import BoardState, UserState
from core.exception import (EntityNotActivatedException,
                            EntityNotAuthorizedException,
                            EntityNotExistException)
from core.model.post import PostCreate, PostUpdate
from utils.htmlUtils import get_clean, get_plain


class PostService:
    @staticmethod
    def create(create: PostCreate, wid, wnick, session: Session):
        # 작성자 위조 방지
        create.writer_id = wid
        create.writer_nick = wnick

        # 사용자 및 게시판 실존 여부 혹은 활성 상태 판단
        user_exist = crud.user.get(id=create.writer_id, session=session)
        board_exist = crud.board.get(id=create.board_id, session=session)

        if board_exist is None:
            raise EntityNotExistException("존재하지 않는 게시판입니다.")

        if board_exist.state != BoardState.ACTIVE:
            raise EntityNotActivatedException("사용할 수 없는 게시판입니다.")

        if user_exist.state != UserState.ACTIVE:
            raise EntityNotActivatedException("차단된 사용자입니다.")

        create: dict = create.dict()
        origin = create.get("body")

        # 금칙어 검사 (제목 + 본문)
        validate(create.get("title") + origin)

        # HTML -> PlainText 파싱, 스크립트/스타일 태그 제거
        cleaned = get_clean(origin)
        plain = get_plain(cleaned)
        create.update({"body": cleaned, "body_plain": plain})

        # 저장
        result = crud.post.create(create=create, session=session)
        return result

    @staticmethod
    def update(update: PostUpdate, wid: int, session: Session):
        target = crud.post.get(id=update.id, session=session)

        # 사용자 및 게시판 실존 여부 혹은 활성상태 판단
        user_exist = crud.user.get(id=target.writer_id, session=session)
        board_exist = crud.board.get(id=target.board_id, session=session)

        if board_exist is None:
            raise EntityNotExistException("존재하지 않는 게시판입니다.")

        if board_exist.state != BoardState.ACTIVE:
            raise EntityNotActivatedException("사용할 수 없는 게시판입니다.")

        if user_exist.state != UserState.ACTIVE:
            raise EntityNotActivatedException("차단된 사용자입니다.")

        if target.writer_id != wid:
            raise EntityNotAuthorizedException("작성자만 게시글을 수정할 수 있습니다.")

        # 금칙어 검사 (제목 + 본문)
        validate(update.title + update.body)

        cleaned = get_clean(update.body)
        plain = get_plain(cleaned)

        target.title = update.title
        target.body = cleaned
        target.body_plain = plain

        session.add(target)
        session.flush()
        session.refresh(target)

        return target

    @staticmethod
    def create_reply():
        pass

    @staticmethod
    def update_reply():
        pass


post = PostService()
