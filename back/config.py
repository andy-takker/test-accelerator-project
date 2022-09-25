from functools import lru_cache
from typing import Optional
from pydantic import BaseSettings, Field, PostgresDsn, validator


class Settings(BaseSettings):

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = Field(default='localhost')
    POSTGRES_PORT: str = Field(default='5432')

    SQLALCHEMY_URL: Optional[PostgresDsn] = None

    @validator('SQLALCHEMY_URL', pre=True)
    def get_sqlalchemy_url(cls, v, values):
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_HOST'),
            port=values.get('POSTGRES_PORT'),
            path=f'/{values.get("POSTGRES_DB")}',
        )



@lru_cache
def get_settings():
    return Settings()