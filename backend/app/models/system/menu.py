from datetime import datetime
from fastapi import Query
from pydantic import BaseModel, Field
from app.models.common import AttachResponseModel, BaseQueryParams


class MenuAddOREditModel(BaseModel):
    key: int | None = Field(None)
    father: int | None = Field(None)
    path: str | None = Field(None)
    title: str | None = Field(None)
    title_mark: str | None = Field(None)
    name: str | None = Field(None)
    redirect: str | None = Field(None)
    icon: str | None = Field(None)
    component: str | None = Field(None)
    order: int | None = Field(None)

    class Config:
        name = 'menu'


class QueryParams(BaseQueryParams):
    def __init__(
            self,
            is_all_query: bool = Query(False),
            uid: str | None = Query(None),
            uids: list[str] | None = Query(None),
            key: int | None = Query(None),
            father: int | None = Query(None),
            path: str | None = Query(None),
            title: str | None = Query(None),
            title_mark: str | None = Query(None),
            name: str | None = Query(None),
            redirect: str | None = Query(None),
            icon: str | None = Query(None),
            component: str | None = Query(None),
            order: int | None = Query(None),
            create_at: list[datetime] = Query(None),
            update_at: list[datetime] = Query(None),
    ):
        self.is_all_query = is_all_query
        self.uid = uid
        self.uids = uids
        self.key = key
        self.father = father
        self.path = path
        self.title = title
        self.title_mark = title_mark
        self.name = name
        self.redirect = redirect
        self.icon = icon
        self.component = component
        self.order = order
        self.create_at = create_at
        self.update_at = update_at


class MenuResponseModel(MenuAddOREditModel, AttachResponseModel):
    pass
