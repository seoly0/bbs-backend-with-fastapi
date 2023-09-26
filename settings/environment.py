from os.path import dirname, join

from pydantic import BaseSettings


class Environment(BaseSettings):

    APP_NAME: str

    APP_AUTHOR_NAME: str
    APP_AUTHOR_EMAIL: str

    ADMIN_PASSWORD: str

    WEB_HOST: str
    API_HOST: str

    CORS_ALLOW_ORIGINS: str

    AES_SECRET: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_EXPIRE: int

    MEDIA_HOST: str
    MEDIA_USER_DEFAULT_THUMBNAIL: str

    USE_AUDIT: bool
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DATABASE: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_KEY: str
    SMTP_USETLS: bool
    SMTP_SENDER: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_TIMEOUT: int
    REDIS_CELERY=str

    MINIO_HOST: str
    MINIO_PORT: int
    MINIO_USER: str
    MINIO_PASSWORD: str

    class Config:
        env_file = join(dirname(__file__), ".env")
        env_file_encoding = "utf-8"
