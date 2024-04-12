from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Set, Dict
from bson import ObjectId
from fastapi.params import Query
from pydantic import BaseModel, Field, AliasChoices


class ResponseModel(BaseModel):
    status_code: int = Field()
    success: bool = Field()
    detail: str = Field()
    data: list[Any] | Any = Field()


class ResponseTotalModel(ResponseModel):
    total: int = Field()


class ResponseLoginModel(ResponseModel):
    access_token: str = Field()
    token_type: str = Field()


class AttachResponseModel(BaseModel):
    id: str | None = Field(None, validation_alias=AliasChoices('_id', 'id'))
    create_at: datetime | None = Field(None)  # 创建时间
    update_at: datetime | None = Field(None)  # 更新时间


class BaseQueryParams:
    def to_dict(self, exclude_none=False, exclude: Set[str] = None) -> Dict[str, Any]:
        """生成查询参数的字典，可选地过滤掉值为None的项，以及排除指定的键。"""
        if exclude is None:
            exclude = set()
        return {
            key: value for key, value in self.__dict__.items()
            if not (exclude_none and value is None) and key not in exclude
        }

    def to_mongo_query(self, exclude_none=True, exclude: Set[str] = None) -> Dict[str, Any]:
        """将查询参数转换为 MongoDB 查询格式。"""

        if exclude is None:
            exclude = set()
        # 过滤查询全部
        exclude.add('is_all_query')

        query_dict = self.to_dict(exclude_none=exclude_none, exclude=exclude)
        mongo_query = {}

        for key, value in query_dict.items():
            # 检查类型生成
            if isinstance(value, datetime):
                # 确保时间是UTC时间
                mongo_query[key] = value.astimezone(timezone.utc)
            elif isinstance(value, (list, tuple, set)):
                # 对于列表、集合或元组，我们使用 $in 语法
                # 对特殊字段进行特殊处理
                if key == 'create_at' or key == 'update_at':
                    mongo_query[key] = {
                        '$gte': value[0].astimezone(timezone.utc),
                        '$lte': value[1].astimezone(timezone.utc)
                    }
                elif key == 'ids' and value is not None:
                    mongo_query['_id'] = {"$in": [ObjectId(v) for v in value]}
                else:
                    mongo_query[key] = {"$in": value}
            elif isinstance(value, dict):
                # 假定字典已经是Mongo查询操作符的格式
                mongo_query[key] = value
            else:
                if key == 'id' and value is not None:
                    mongo_query['_id'] = ObjectId(value)
                else:
                    mongo_query[key] = value

        return mongo_query


@dataclass
class PagingQueryParams(BaseQueryParams):
    current_page: int = Query(1)
    page_size: int = Query(10)

    def to_mongo_query(self, exclude_none=True, exclude: Set[str] = None) -> Dict[str, Any]:
        # 预定义要排除的字段
        exclude = exclude or set()
        exclude.update({'current_page', 'page_size'})
        return super().to_mongo_query(exclude_none=exclude_none, exclude=exclude)
