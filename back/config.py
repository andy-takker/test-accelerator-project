from functools import lru_cache
from typing import Any, Dict, Optional

from pydantic import BaseSettings, Field, PostgresDsn, RedisDsn, validator


class Settings(BaseSettings):

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: str = Field(default="5432")

    SQLALCHEMY_URL: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_URL", pre=True)
    def get_sqlalchemy_url(cls, v, values):
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f'/{values.get("POSTGRES_DB")}',
        )

    REDIS_HOST: str = Field(default="redis")
    REDIS_PORT: str = Field(default="6379")
    REDIS_PASSWORD: str = Field(default="secret")

    REDIS_URI: Optional[RedisDsn] = None

    @validator("REDIS_URI", pre=True)
    def assemble_redis_uri(cls, v: Optional[str], values: Dict[str, str]) -> Any:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme="redis",
            host=values.get("REDIS_HOST"),
            port=values.get("REDIS_PORT"),
            password=values.get("REDIS_PASSWORD"),
        )


@lru_cache
def get_settings():
    return Settings()
