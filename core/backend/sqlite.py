import time
from functools import wraps
from logging import getLogger

from env import CONFIG
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session, sessionmaker  # noqa

logger = getLogger("data")

SQL_URI = CONFIG.SQLITE.uri

engine = create_engine(
    SQL_URI,
    connect_args={"check_same_thread": False},
)

SessionProvider = sessionmaker(autocommit=False, autoflush=False, bind=engine)
