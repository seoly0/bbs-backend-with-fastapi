from .base import Entity, BaseMixin
from sqlalchemy import Column, String, Integer


class CrawlPostBasic:
    target_id = Column(Integer)
    url = Column(String)
    post_id = Column(Integer)
    type = Column(String)


class CrawlPost(Entity, BaseMixin, CrawlPostBasic):
    pass
