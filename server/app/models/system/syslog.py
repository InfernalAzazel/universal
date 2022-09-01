from datetime import datetime
from typing import TYPE_CHECKING, Any
from pydantic import BaseModel


class SysLog(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)
        for k, v in data.items():
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

    username: str = None
    host: str = None
    browser: str = None
    os: str = None
    path: str = None
    query_params: str = None
    method: str = None
    text: str = None