from pydantic import BaseModel


class Init(BaseModel):
    switch: bool


class Shared(BaseModel):
    tz_info: str


class Mongodb(BaseModel):
    host: str
    username: str
    password: str


class Jwt(BaseModel):
    secret_key: str
    algorithm: str
    minutes: int


class Settings(BaseModel):
    init: Init
    shared: Shared
    mongodb: Mongodb
    jwt: Jwt
