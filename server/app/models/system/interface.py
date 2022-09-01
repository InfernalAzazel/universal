from datetime import datetime
from typing import TYPE_CHECKING, Any
from pydantic import BaseModel


class Interface(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)
        for k, v in list(data.items()):
            match k:
                case "_id":
                    self.__dict__['uid'] = str(data[k])
                case _:
                    self.__dict__[k] = data[k]

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    if TYPE_CHECKING:
        uid: str = None
        create_at: datetime = None  # 创建时间
        update_at: datetime = None  # 更新时间
    path: str
    group: str
    describe_zh_cn: str
    describe_en_us: str
    method: str


class SearchInterface(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)
        for k, v in list(data.items()):
            if k == '_id':
                self.__dict__['uid'] = str(data[k])
                self.__dict__['describe'] = str(data[k])
            elif v == '':
                self.__dict__[k] = None
            else:
                self.__dict__[k] = v

    if TYPE_CHECKING:
        uid: str = None
    path: str = None
    group: str = None
    describe_zh_cn: str = None
    describe_en_us: str = None
    method: str = None
