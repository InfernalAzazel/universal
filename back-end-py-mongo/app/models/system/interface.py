from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, Field

from app.models.common import AttachResponseModel, BaseQueryParams


class InterfaceAddOREditModel(BaseModel):
    title: str | None = Field(None)
    path: str | None = Field(None)
    group: str | None = Field(None)
    method: str | None = Field(None)

    class Config:
        name = 'interface'


class QueryParams(BaseQueryParams):
    def __init__(
            self,
            is_all_query: bool = Query(False),
            uid: str | None = Query(None),
            title: str | None = Query(None),
            path: str | None = Query(None),
            group: str | None = Query(None),
            method: str | None = Query(None),
            create_at: list[datetime] = Query(None),
            update_at: list[datetime] = Query(None),
    ):
        self.is_all_query = is_all_query
        self.uid = uid
        self.title = title
        self.path = path
        self.group = group
        self.method = method
        self.create_at = create_at
        self.update_at = update_at


class InterfaceResponseModel(InterfaceAddOREditModel, AttachResponseModel):
    pass
