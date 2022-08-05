from datetime import datetime
from typing import TYPE_CHECKING, Any
from pydantic import BaseModel


class Menu(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)
        for k, v in data.items():
            match k:
                case "_id":
                    self.__dict__['id'] = str(data['_id'])
                case "role_id":
                    self.__dict__[k] = str(data[k])
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
        role_id: str = None
        create_at: datetime = None  # 创建时间
        update_at: datetime = None  # 更新时间
    key: int
    father: int
    path: str
    title_zh_cn: str
    title_en_us: str
    icon: str
    component: str
    order: int


class SearchMenu(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)
        for k, v in data.items():
            match v:
                case '':
                    self.__dict__[k] = None
                case _:
                    self.__dict__[k] = data[k]

    if TYPE_CHECKING:
        id: str = None
    key: int = None
    father: int = None
    hide: bool = None
    path: str = None
    title_zh_cn: str = None
    title_en_us: str = None
    icon: str = None
    component: str = None
