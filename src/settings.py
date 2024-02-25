from pathlib import Path

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    PROJECT_DIR: Path

    DEBUG: bool

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    VK_TOKENS: str | list[str]
    ADMINS: str | list[int]

    @validator("VK_TOKENS")
    def vk_tokens_validator(cls, v: str) -> list[str]:  # noqa
        return v.split(" ")

    @validator("ADMINS")
    def admins_validator(cls, v: str) -> list[int]:  # noqa
        return list(map(int, v.split(" ")))


settings = Settings()
