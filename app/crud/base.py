from typing import Generic, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy import update as orm_update
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from core.entity import AuditMixin, BaseMixin, Entity
from core.exception import EntityNotAuthorizedException, EntityNotExistException
from core.http.request import Page, Pagination
from settings import ENV

EntityType = TypeVar("EntityType", bound=BaseMixin)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
AuditType = TypeVar("AuditType", bound=AuditMixin)


class CRUDBase(Generic[EntityType, AuditType]):
    def __init__(self, entity: Type[EntityType], audit: Type[AuditType] | None = None):
        self.entity = entity
        self.audit = audit

    def get(
        self,
        id: int,
        session: Session = None,
        check: tuple | list | None = None,
        exc: Exception = EntityNotAuthorizedException,
    ) -> Optional[EntityType]:
        result = session.scalar(select(self.entity).where(self.entity.deleted == False, self.entity.id == id))

        if result:
            if check:
                if getattr(result, check[0]) != check[1]:
                    raise exc
            return result
        else:
            return None

    def get_list(
        self,
        filter=None,
        order=None,
        limit: int = None,
        session: Session = None,
    ) -> list[EntityType]:
        query = select(self.entity).where(self.entity.deleted == False)
        if filter is not None:
            if hasattr(filter, "__iter__"):
                query = query.where(*filter)
            else:
                query = query.where(filter)

        if order is not None:
            if hasattr(order, "__iter__"):
                query = query.order_by(*order)
            else:
                query = query.order_by(order)
        else:
            # list는 asc로 기본정렬
            query = query.order_by(self.entity.id.asc())
        if limit is not None:
            query = query.limit(limit)

        result = session.scalars(query).all()
        return result if result else []

    def get_page(self, page: Page, filter=None, order=None, session: Session = None) -> Pagination[EntityType]:
        number = page.page
        offset = number - 1
        size = page.size
        query = select(self.entity).where(self.entity.deleted == False)

        if filter is not None:
            if hasattr(filter, "__iter__"):
                query = query.where(*filter)
            else:
                query = query.where(filter)

        if order is not None:
            if hasattr(order, "__iter__"):
                query = query.order_by(*order)
            else:
                query = query.order_by(order)
        else:
            # page는 desc로 기본정렬
            query = query.order_by(self.entity.id.desc())

        contents = session.scalars(query.offset(offset * size).limit(size)).all()
        total = session.scalar(select(func.count("*")).select_from(query))
        result = Pagination(
            contents=contents,
            page=number,
            size=size,
            total=total,
            pages=(total // page.size) + (1 if total % page.size != 0 else 0),
        )
        return result

    def create(self, create: CreateSchemaType, session: Session) -> EntityType:
        if isinstance(create, dict):
            create_dict = create
        elif isinstance(create, BaseModel):
            create_dict = create.dict(exclude_unset=True)
        elif isinstance(create, Entity):
            create_dict = create.__dict__
        else:
            raise ValueError

        result = session.scalar(insert(self.entity).returning(self.entity), [create_dict])
        self.record(result, session=session)
        return result

    def update(
        self,
        update: UpdateSchemaType | dict[str, any],
        session: Session,
        check: tuple | list | None = None,
        exc: Exception = EntityNotAuthorizedException,
    ) -> EntityType:
        if isinstance(update, dict):
            update_dict = update
        elif isinstance(update, BaseModel):
            update_dict = update.dict(exclude_unset=True)
        elif isinstance(update, Entity):
            update_dict = update.__dict__
        else:
            raise ValueError

        obj: EntityType = session.scalar(
            select(self.entity).where(self.entity.deleted == False, self.entity.id == update_dict.get("id"))
        )

        if check:
            if getattr(obj, check[0]) != check[1]:
                raise exc

        result = session.scalar(
            orm_update(self.entity)
            .where(self.entity.deleted == False, self.entity.id == update_dict.get("id"))
            .values(**update_dict)
            .returning(self.entity)
        )
        self.record(result, session=session)
        return result

    def remove(self, id: int, session: Session, check: tuple | list | None = None) -> EntityType:
        obj: EntityType = session.scalar(select(self.entity).where(self.entity.deleted == False, self.entity.id == id))

        if obj is None:
            raise EntityNotExistException

        if check:
            if getattr(obj, check[0]) != check[1]:
                raise EntityNotAuthorizedException

        result = session.scalar(
            orm_update(self.entity)
            .where(self.entity.deleted == False, self.entity.id == id)
            .values({"deleted": True})
            .returning(self.entity)
        )
        self.record(result, session=session)

        return True

    def record(self, data: EntityType, session: Session, created_by: int = 0, updated_by: int = 0) -> None:
        if self.audit is not None and ENV.USE_AUDIT:
            data_to_json = jsonable_encoder(data)
            aud = self.audit(**data_to_json)
            aud.created_by = created_by
            aud.updated_by = updated_by
            obj = aud.__dict__
            session.execute(insert(self.audit), [obj])

        return True
