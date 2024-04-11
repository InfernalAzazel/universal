from typing import Any

from bson import ObjectId
from pydantic import BaseModel


# 导出
class ExportDB(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)
        for k, v in data.items():
            match k:
                case "_id":
                    self.__dict__[k] = str(data[k])
                case _:
                    self.__dict__[k] = data[k]


# 导入
class ImportDB(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)
        for k, v in data.items():
            match k:
                case "_id":
                    self.__dict__[k] = ObjectId(data[k])
                case _:
                    self.__dict__[k] = data[k]
