from pydantic import BaseModel
from typing import List


class _Database(BaseModel):
    url: str


class _Bot(BaseModel):
    admins: List[int]
    tokens: List[str]


class _VK(BaseModel):
    bot: _Bot


class ConfigModel(BaseModel):
    database: _Database
    vk: _VK
