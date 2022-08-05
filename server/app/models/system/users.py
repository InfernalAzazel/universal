from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel


class AssociationRole(BaseModel):
    id: str = None  # id
    name_zh_cn: str = None  # 中文名称
    name_en_us: str = None  # 英文名称


class User(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)
        for k, v in list(data.items()):
            match k:
                case "_id":
                    self.__dict__['id'] = str(data[k])
                case "association_role":
                    self.__dict__[k] = AssociationRole(**v)
                case _:
                    self.__dict__[k] = v

    def __setattr__(self, key, value):
        match key:
            case 'create_at':
                self.__dict__[key] = value
            case 'update_at':
                self.__dict__[key] = value

    if TYPE_CHECKING:
        id: str = None  # id
        name: str = None  # 姓名:  张三
        mail: str = None  # 邮箱
        company: str = None  # 公司
        department: str = None  # 部门
        association_role: AssociationRole = None  # 关联角色
        create_at: datetime = None  # 创建时间
        update_at: datetime = None  # 更新时间

    username: str = None  # 帐号： quid1111
    disabled: bool = None  # 禁用：True == 禁用


class CreateUser(User):
    password: str = None  # 密码： 123456
