import time
from functools import wraps
from logging import INFO, getLogger

from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql.base import PGCompiler
from sqlalchemy.engine import Connection
from sqlalchemy.orm import sessionmaker  # noqa

from settings import ENV

# python 3.8 이하는 psycopg2 필요
# python 3.9 이상은 psycopg2-binary 필요

logger = getLogger("data")

POSTGRES_URL = f"postgresql://{ENV.POSTGRES_USER}:{ENV.POSTGRES_PASSWORD}@{ENV.POSTGRES_HOST}:{ENV.POSTGRES_PORT}/{ENV.POSTGRES_DATABASE}"

engine = create_engine(
    POSTGRES_URL,
    echo=False,
    connect_args={"options": "-c timezone=Asia/Seoul", "connect_timeout": 5},
)

SessionProvider = sessionmaker(autoflush=True, bind=engine)
