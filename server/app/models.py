from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel


class User(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)
        for k, v in list(data.items()):
            if k == "_id":
                self.__dict__['id'] = str(data[k])
                data.pop(k)
            else:
                self.__dict__[k] = v

    if TYPE_CHECKING:
        id: str = None  # id
        role_id: str = None  # 角色id
        role_name: str = None  # 角色名称： 普通用户
        name: str = None  # 姓名:  张三
        mail: str = None  # 邮箱
        company: str = None  # 公司
        department: str = None  # 部门
        menu_nodes: list[dict] = None  # 用户的菜单
        create_time: datetime = None  # 创建时间

    username: str = None  # 帐号： quid1111
    disabled: bool = None  # 禁用：True == 禁用


class CreateUser(User):
    password: str = None  # 密码： 123456


class Role(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)
        for k, v in data.items():
            if k == '_id':
                self.__dict__['id'] = str(data['_id'])
            else:
                self.__dict__[k] = data[k]

    if TYPE_CHECKING:
        id: str = None
    key: str
    name: str
    description: str
    menu_nodes: list[dict] = []
    interface_nodes: list[dict] = []
