from sqlalchemy import select
from sqlalchemy.orm import Session

from core.entity import Contact, ContactAud, ContactCategory, ContactCategoryAud, User
from core.model.contact import ContactCreate

from .base import CRUDBase


class ContactCRUD(CRUDBase[Contact, ContactAud]):
    def create(self, create: ContactCreate, session: Session) -> Contact:
        user = session.scalar(select(User).where(User.id == create.user_id, User.deleted == False))
        cat = session.scalar(
            select(ContactCategory).where(ContactCategory.id == create.category_id, ContactCategory.deleted == False)
        )

        if user and cat:
            obj = super().create(create, session)
        else:
            # TODO raise Exception
            obj = None

        return obj


class ContactCategoryCRUD(CRUDBase[ContactCategory, ContactCategoryAud]):
    pass


contact = ContactCRUD(Contact, ContactAud)
contact_category = ContactCategoryCRUD(ContactCategory, ContactCategoryAud)
