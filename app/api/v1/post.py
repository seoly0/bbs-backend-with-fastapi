from logging import getLogger

from fastapi import APIRouter, Depends, status
from sqlalchemy import and_, or_

from app import crud, service
from app.batch.banning.methods import validate
from core.auth import has_role
from core.entity import Post, PostReply
from core.enum import PostState
from core.exception import ResponseNoneException, SearchTooShortException
from core.http.request import Page, Pagination, Request
from core.model.post import (PostCreate, PostDetail, PostMeta, PostMetaForBest,
                             PostReplyCreate, PostReplyDefault,
                             PostReplyUpdate, PostUpdate)
from utils.pathUtils import parse_order

logger = getLogger(__name__)

router = APIRouter()
router.tags = ["게시글"]
router.prefix = "/post"


@router.get(path="", name="게시글 보기", response_model=PostDetail)
def serve_post_by(req: Request, id: int):
    """
    - **id**: 조회할 게시글의 id
    """
    # 따봉여부 판단을 위한 uid 추출
    uid = None
    if req.state.auth:
        uid = req.state.auth.id

    result = crud.post.get_with(pid=id, uid=uid, session=req.state.backend)

    if result:
        if result.deleted:
            raise ResponseNoneException("삭제된 게시글입니다.")
        elif result.state == PostState.ACCUSED:
            raise ResponseNoneException("신고 누적으로 차단된 게시글입니다.")
        elif result.state == PostState.BLOCKED:
            raise ResponseNoneException("관리자에 의해 차단된 게시글입니다.")

        crud.post.increase_view_cnt(id=id, session=req.state.backend)

    else:
        raise ResponseNoneException("게시글이 존재하지 않습니다.")

    return result


@router.get(path="/search/list/page", name="게시글 검색 페이지 목록", response_model=Pagination[PostMeta])
def serve_post_search(
    req: Request,
    query: str,
    board_id: int | None = None,
    criteria: str = "T",
    page: Page = Depends(),
):
    """
    - **query**: 검색어
    - **criteria**: 검색 대상, A - 전체, T - 제목, B - 본문, W - 작성자, ex) 제목검색 -> T, 전체검색 -> A, 제목 + 본문 검색 -> TB 또는 BT
    - **writer_id**: 해당 사용자의 게시글 목록, 0 일시 모든 사용자의 게시글
    - **board_id**: 해당 게시판의 게시글 목록, 0 일시 모든 게시판의 게시글
    - **page**: 현재 페이지 넘버
    - **size**: 각 페리지의 크기
    - **order**: 정렬방식, 현재 미지원
    """
    if len(query) < 2:
        raise SearchTooShortException

    filter = []
    # criteria type: A - 전체, T - 제목, B - 본문, W - 작성자
    if criteria == "A" or criteria.find("T") > -1:
        filter.append(Post.title.contains(query))
    if criteria == "A" or criteria.find("B") > -1:
        filter.append(Post.body_plain.contains(query))
    if criteria == "A" or criteria.find("W") > -1:
        filter.append(Post.writer_nick.contains(query))

    filter = or_(*filter)

    if board_id:
        filter = and_(Post.board_id == board_id, filter)

    return crud.post.get_page(page=page, filter=filter, session=req.state.backend)


@router.get(path="/list/page", name="게시글 페이지 목록", response_model=Pagination[PostMeta])
def serve_post_page(req: Request, page: Page = Depends(), writer_id: int | None = None, board_id: int | None = None):
    """
    - **writer_id**: 해당 사용자의 게시글 목록, 0 일시 모든 사용자의 게시글
    - **board_id**: 해당 게시판의 게시글 목록, 0 일시 모든 게시판의 게시글
    - **page**: 현재 페이지 넘버
    - **size**: 각 페리지의 크기
    - **order**: 정렬방식, 현재 미지원
    """

    # logger.debug()
    # query_order =

    filter = []
    if writer_id:
        filter.append(Post.writer_id == writer_id)
    if board_id:
        filter.append(Post.board_id == board_id)

    return crud.post.get_page(
        page=page,
        session=req.state.backend,
        order=parse_order(Post, page.order),
        filter=and_(*filter),
    )


@router.get(path="/best/list/page", name="베스트 게시글 페이지 목록", response_model=Pagination[PostMetaForBest])
def serve_best_post_page(req: Request, page: Page = Depends(), board_id: int | None = None):
    """
    게시글이 작성되고 24시간 이내에 추천 5개 이상을 받으면 베스트에 등록됨
    - **board_id**: 해당 게시판의 게시글 목록, 0 일시 모든 게시판의 베스트 게시글
    - **page**: 현재 페이지 넘버
    - **size**: 각 페리지의 크기
    - **order**: 정렬방식, 현재 미지원
    """
    filter = [Post.best == True]
    if board_id:
        filter.append(Post.board_id == board_id)

    return crud.post.get_page(
        page=page, session=req.state.backend, filter=and_(*filter), order=(Post.best_at.desc(), Post.id.desc())
    )


@router.get(path="/new/list", name="신규 게시글 목록", response_model=list[PostMeta])
def serve_new_post_list(req: Request, size: int = 5):
    return crud.post.get_list(limit=size, order=Post.id.desc(), session=req.state.backend)


@router.get(path="/best/list", name="베스트 게시글 목록", response_model=list[PostMetaForBest])
def serve_new_post_list(req: Request, size: int = 5):
    return crud.post.get_list(
        filter=Post.best == True, limit=size, order=(Post.best_at.desc(), Post.id.desc()), session=req.state.backend
    )


@router.post(path="", name="게시글 생성", status_code=status.HTTP_201_CREATED)
@has_role(["USER"])
def create_post(
    req: Request,
    create: PostCreate,
):
    """
    - **title**: 게시글 제목
    - **body**: 게시글 내용
    - **board_id**: 게시판 id
    - **writer_id**: 작성자 id / 서버에서 처리하므로 0 등 아무값
    - **writer_nick**: 작성자 닉네임 / 서버에서 처리하므로 빈문자열 등 아무값
    """
    return service.post.create(
        create=create, wid=req.state.auth.id, wnick=req.state.auth.extra.get("nick"), session=req.state.backend
    )


@router.put(
    path="",
    name="게시글 수정",
)
@has_role(["USER"])
def update_post(
    req: Request,
    update: PostUpdate,
):
    """
    - **id**: 수정할 게시글 id
    - **title**: 수정된 게시글 제목
    - **body**: 수정된 게시글 내용
    """
    return service.post.update(update=update, wid=req.state.auth.id, session=req.state.backend)


@router.delete(
    path="",
    name="게시글 삭제",
)
@has_role(["USER"])
def delete_post(
    req: Request,
    id: int,
):
    """
    - **id**: 삭제할 게시글의 id
    """
    return crud.post.remove(id=id, session=req.state.backend, check=("writer_id", req.state.auth.id))


# by post or writer
@router.get(path="/reply", name="댓글만", response_model=list[PostReplyDefault])
def serve_reply(req: Request, post_id: int):
    """ """
    # 따봉여부 판단을 위한 uid 추출
    uid = None
    if req.state.auth:
        uid = req.state.auth.id

    return crud.post_reply.get_replies(pid=post_id, uid=uid, session=req.state.backend)


@router.post(path="/reply", name="게시글에 댓글 생성")
@has_role(["USER"])
def create_reply(
    req: Request,
    create: PostReplyCreate,
):
    """
    - **target_id**: target은 임의의 댓글이며, 이 댓글은 target의 대댓글임을 의미함. 대댓글이 아닌 일반 댓글인 경우 0
    - **post_id**: 이 댓글이 어느 게시글의 댓글인지를 의미함.
    - **writer_id**: 작성자 id / 서버에서 처리하므로 아무값.
    - **writer_nick**: 작성자 닉네임 / 서버에서 처리하므로 아무값.
    - **body**: 댓글 본문.
    """
    validate(create.body)

    # 작성자 위조 방지
    create.writer_id = req.state.auth.id
    create.writer_nick = req.state.auth.extra.get("nick")
    if create.target_id == 0:
        create.target_id = None
    result = crud.post_reply.create(create=create, session=req.state.backend)
    session = req.state.backend

    replies_cnt = (
        session.query(PostReply).filter(PostReply.post_id == create.post_id, PostReply.deleted == False).count()
    )

    post = session.query(Post).get(create.post_id)
    post.replies_cnt = replies_cnt
    session.add(post)
    session.flush()

    return result


@router.put(path="/reply", name="게시글에 댓글 수정")
@has_role(["USER"])
def update_reply(
    req: Request,
    update: PostReplyUpdate,
):
    """
    - **id**: 수정할 댓글의 id.
    - **body**: 댓글 본문.
    """
    validate(update.body)
    return crud.post_reply.update(update=update, session=req.state.backend, check=("writer_id", req.state.auth.id))


@router.delete(path="/reply", name="게시글에 댓글 삭제")
@has_role(["USER"])
def delete_reply(
    req: Request,
    id: int,
):
    """
    - **id**: 삭제할 댓글 id
    """
    return crud.post_reply.remove(id=id, session=req.state.backend, check=("writer_id", req.state.auth.id))
