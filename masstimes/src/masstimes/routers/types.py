from pydantic import BaseModel


class AdminConfig(BaseModel):
    username: str
    password: str


class Config(BaseModel):
    admin: AdminConfig
