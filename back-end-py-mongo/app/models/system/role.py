from datetime import datetime
from typing import List, Any

from fastapi.params import Query
from pydantic import BaseModel, Field
from app.models.common import AttachResponseModel, BaseQueryParams


class RoleAddOREditModel(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    menu_permission: List[str] | None = Field(None)
    interface_permission: list[str] | None = Field(None)

    class Config:
        name = 'role'


class QueryParams(BaseQueryParams):
    def __init__(
            self,
            is_all_query: bool = Query(False),
            uid: str | None = Query(None),
            description: str | None = Query(None),
            create_at: list[datetime] = Query(None),
            update_at: list[datetime] = Query(None)
    ):
        self.is_all_query = is_all_query
        self.uid = uid
        self.description = description
        self.create_at = create_at
        self.update_at = update_at


class RoleResponseModel(RoleAddOREditModel, AttachResponseModel):
    pass
