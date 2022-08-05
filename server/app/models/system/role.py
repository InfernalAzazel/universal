from datetime import datetime
from typing import TYPE_CHECKING, Any
from pydantic import BaseModel


class Role(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)
        for k, v in data.items():
            match k:
                case "_id":
                    self.__dict__['id'] = str(data[k])
                case _:
                    self.__dict__[k] = data[k]

    def __setattr__(self, key, value):
        match key:
            case 'create_at':
                self.__dict__[key] = value
            case 'update_at':
                self.__dict__[key] = value

    if TYPE_CHECKING:
        id: str = None
        create_at: datetime = None  # 创建时间
        update_at: datetime = None  # 更新时间
    name_zh_cn: str
    name_en_us: str
    describe: str
    menu_permission: list[dict] = []
    interface_permission: list[dict] = []


class SearchRole(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)
        for k, v in data.items():
            match v:
                case '':
                    self.__dict__[k] = None
                case _:
                    self.__dict__[k] = data[k]

    name_zh_cn: str = None
    name_en_us: str = None
