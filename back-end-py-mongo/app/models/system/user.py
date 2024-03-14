from datetime import datetime

from fastapi import Query
from pydantic import BaseModel

from app.models.common import AttachResponseModel, BaseQueryParams


class UserEditModel(BaseModel):
    username: str | None = None  # 帐号： quid1111
    disabled: bool | None = None  # 禁用：True == 禁用
    role_names: list[str] | None = None  # 关联角色
    name: str | None = None  # 姓名:  张三
    mail: str | None = None  # 邮箱
    company: str | None = None  # 公司
    department: str | None = None  # 部门

    class Config:
        name = 'users'


class QueryParams(BaseQueryParams):
    def __init__(
            self,
            uid: str | None = Query(None),
            username: str | None = Query(None),
            disabled: bool | None = Query(None),
            role_names: list[str] | None = Query(None),
            name: str | None = Query(None),
            mail: str | None = Query(None),
            company: str | None = Query(None),
            department: str | None = Query(None),
            create_at: list[datetime] = Query(None),
            update_at: list[datetime] = Query(None)
    ):
        self.uid = uid
        self.username = username
        self.disabled = disabled
        self.role_names = role_names
        self.name = name
        self.mail = mail
        self.company = company
        self.department = department
        self.create_at = create_at
        self.update_at = update_at


class UserAddModel(UserEditModel):
    password: str = None  # 密码： 123456


class UserResponseModel(UserEditModel, AttachResponseModel):
    pass
