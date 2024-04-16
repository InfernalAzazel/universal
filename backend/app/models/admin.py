from dataclasses import dataclass
from datetime import datetime

from beanie import Document
from fastapi import Query
from pydantic import Field, BaseModel

from app.models.common import BaseQueryParams
from app.utils.mixin import DBMixin


# ----------------- 系统 --------------------------
class User(DBMixin, Document):
    username: str = Field()  # 帐号： quid1111
    password: str = Field()  # 密码
    disabled: bool = Field(False)  # 禁用：True == 禁用
    is_super: bool = Field(False)  # 是否为超级管理员
    role_names: list[str] = Field([])  # 关联角色
    name: str | None = Field(None)  # 姓名:  张三
    mail: str | None = Field(None)  # 邮箱
    company: str | None = Field(None)  # 公司
    department: str | None = Field(None)  # 部门

    class Settings:
        name = "users"


@dataclass
class UserQueryParams(BaseQueryParams):
    is_all_query: bool = Query(False)
    id: str = Query(None)
    username: str = Query(None)
    role_names: list[str] = Query(None)
    name: str = Query(None)
    mail: str = Query(None)
    company: str = Query(None)
    department: str = Query(None)
    create_at: list[datetime] = Query(None)
    update_at: list[datetime] = Query(None)


class UserCreateBody(BaseModel):
    username: str = Field()
    password: str = Field()
    disabled: bool = Field(False)
    role_names: list[str] = Field([])


class UserEditBody(BaseModel):
    title: str = Field(None)
    description: str = Field(None)
    menu_permission: list[str] = Field([])
    interface_permission: list[str] = Field([])


class Role(DBMixin, Document):
    title: str | None = Field(None)
    description: str | None = Field(None)
    is_super: bool = Field(False)  # 是否超级管理员
    menu_permission: list[str] = Field([])
    interface_permission: list[str] = Field([])

    class Settings:
        name = "role"


@dataclass
class RoleQueryParams(BaseQueryParams):
    is_all_query: bool = Query(False)
    id: str = Query(None)
    title: str = Query(None)
    description: str = Query(None)
    create_at: list[datetime] = Query(None)
    update_at: list[datetime] = Query(None)


class RoleCreateBody(BaseModel):
    title: str = Field()
    description: str = Field()


class RoleEditBody(BaseModel):
    title: str = Field(None)
    description: str = Field(None)
    menu_permission: list[str] = Field([])
    interface_permission: list[str] = Field([])


class Interface(DBMixin, Document):
    title: str = Field()
    path: str = Field()
    group: str = Field()
    method: str = Field()

    class Settings:
        name = "interface"


@dataclass
class InterfaceQueryParams(BaseQueryParams):
    is_all_query: bool = Query(False)
    id: str = Query(None)
    title: str = Query(None)
    path: str = Query(None)
    group: str = Query(None)
    method: str = Query(None)
    create_at: list[datetime] = Query(None)
    update_at: list[datetime] = Query(None)


class InterfaceCreateBody(BaseModel):
    title: str = Field()
    path: str = Field()
    group: str = Field()
    method: str = Field()


class InterfaceEditBody(BaseModel):
    title: str = Field(None)
    path: str = Field(None)
    group: str = Field(None)
    method: str = Field(None)


class Menu(DBMixin, Document):
    key: int = Field()
    father: int = Field()
    path: str = Field()
    title: str = Field()
    title_mark: str = Field()
    name: str | None = Field(None)
    redirect: str | None = Field(None)
    icon: str | None = Field(None)
    component: str = Field()
    order: int = Field()

    class Settings:
        name = "menu"


@dataclass
class MenuQueryParams(BaseQueryParams):
    is_all_query: bool = Query(False)
    id: str | None = Query(None)
    ids: list[str] | None = Query(None)
    key: int | None = Query(None)
    father: int | None = Query(None)
    path: str | None = Query(None)
    title: str | None = Query(None)
    title_mark: str | None = Query(None)
    name: str | None = Query(None)
    redirect: str | None = Query(None)
    icon: str | None = Query(None)
    component: str | None = Query(None)
    order: int | None = Query(None)
    create_at: list[datetime] | None = Query(None)
    update_at: list[datetime] | None = Query(None)


class MenuCreateBody(BaseModel):
    key: int = Field()
    father: int = Field()
    path: str = Field()
    title: str = Field()
    title_mark: str = Field()
    name: str | None = Field(None)
    redirect: str | None = Field(None)
    icon: str | None = Field(None)
    component: str = Field()
    order: int = Field()


class MenuEditBody(BaseModel):
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
