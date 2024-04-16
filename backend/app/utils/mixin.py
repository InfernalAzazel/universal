from datetime import datetime

import bson
from beanie import before_event, Save, Update, Replace, Insert, Document
from pydantic import BaseModel, Field
from typing_extensions import Mapping

from app.utils.api_response import APIResponse, StatusCode, DefaultCodes
from typing import Type, Any


class DBMixin(BaseModel):
    create_at: datetime = Field(default_factory=datetime.utcnow)
    update_at: datetime = Field(default_factory=datetime.utcnow)

    @before_event(Save)
    async def before_save(self):
        """ 保存修改一条 """
        self.update_at = datetime.utcnow()

    @before_event(Update)
    async def before_update(self) -> None:
        """ 更新一条  """
        self.update_at = datetime.utcnow()

    @before_event(Replace)
    async def before_replace(self) -> None:
        """ 替换一条 """
        self.update_at = datetime.utcnow()

    @before_event(Insert)
    async def before_insert(self) -> None:
        """ 插入单条 """
        self.create_at = datetime.utcnow()

    @staticmethod
    async def paginate_queryset(queryset: Type[Document], query: dict, ppq):
        skip = (ppq.current_page - 1) * ppq.page_size
        q = queryset.find(query)
        obj = await q.skip(skip).limit(ppq.page_size).to_list()
        total = await q.count()
        return obj, total

    @staticmethod
    async def crud_list(
            queryset: Type[Document],
            qp,
            ppq,
            exclude: set[int] | set[str] | dict[int, Any] | dict[str, Any] | None = None
    ) -> APIResponse:
        """
        分页查询或返回全部数据。

        Args:
            queryset (Type[Document]): 操作的 MongoDB 文档类。
            qp: 包含查询参数，具体依赖于其 to_mongo_query 方法的实现。
            ppq: 另一组查询参数，可能用于权限过滤等，具体依赖于其 to_mongo_query 方法的实现。
            exclude: 设置需要过滤的字段，默认 None

        Returns:
            APIResponse: 包含查询结果和状态信息的响应对象。
        """
        try:
            # 合并两个查询参数生成最终的查询条件
            qp_query = qp.to_mongo_query()
            query = {**qp_query, **ppq.to_mongo_query()}
        except bson.errors.InvalidId:
            # 如果查询参数中包含无效的 MongoDB ObjectId，返回错误响应
            return APIResponse(code=StatusCode.not_valid_object_id.value)

        if not qp.is_all_query:
            # 如果不是请求全部数据，执行分页查询
            obj, total = await DBMixin.paginate_queryset(queryset, query, ppq)
            data = [d.dict(exclude=exclude) for d in obj]
            return APIResponse(data, total=total)

        # 如果请求全部数据，查询并返回所有符合条件的数据
        obj = await queryset.find(query).to_list()
        data = [d.dict(exclude=exclude) for d in obj]
        return APIResponse(data)

    @staticmethod
    async def crud_add(
            queryset: Type[Document],
            body: BaseModel,
            codes: DefaultCodes,
            query_filter: Mapping[str, Any] | bool | None = None
    ) -> APIResponse:
        """
        向数据库添加一条记录

        Note:
          - `query_filter` 使用时，Document 查询不支持直接通过 ID 查询, 如果需要通过 ID 进行过滤，请使用原生 dict

        Args:
            queryset: 操作的文档类。
            body: 包含数据模型的基础模型实例。
            codes: 成功代码标志, 失败代码标志, 找不到数据代码标志
            query_filter: 用于查找记录的过滤器字典, 如果提供，且记录已存在则不添加。

        Returns:
            APIResponse: 包含操作结果的响应对象
        """
        b = body.model_dump()

        if query_filter:
            existing_record = await queryset.find_one(query_filter)
            if existing_record:
                return APIResponse(code=codes.not_found_code)

        result = await queryset(**b).save()

        if not result:
            return APIResponse(code=codes.failed_add_code)

        return APIResponse(result, success=True, code=codes.success_add_code)

    @staticmethod
    async def crud_retrieve(
            queryset: Type[Document],
            data_id: str,
            codes: DefaultCodes,
            exclude: set[int] | set[str] | dict[int, Any] | dict[str, Any] | None = None,
    ):
        """
        向数据库编辑一条记录

        Args:
            queryset: 操作的文档类
            data_id: 数据 ID
            body: 包含数据模型的基础模型实例
            codes: 成功代码标志, 失败代码标志, 找不到数据代码标志
            exclude: 设置需要过滤的字段，默认 None
        Returns:
            APIResponse: 包含操作结果的响应对象
        """

        result = await queryset.get(data_id)

        if not result:
            return APIResponse(code=codes.failed_retrieve_code)
        return APIResponse(result.dict(exclude=exclude), success=True, code=codes.success_retrieve_code, exclude=exclude)

    @staticmethod
    async def crud_edit(
            queryset: Type[Document],
            data_id: str,
            body: BaseModel,
            codes: DefaultCodes
    ):
        """
        向数据库编辑一条记录

        Args:
            queryset: 操作的文档类
            data_id: 数据 ID
            body: 包含数据模型的基础模型实例
            codes: 成功代码标志, 失败代码标志, 找不到数据代码标志

        Returns:
            APIResponse: 包含操作结果的响应对象
        """
        update_data = {'$set': body.model_dump(exclude_none=True)}
        existing_record = await queryset.get(data_id)

        if not existing_record:
            return APIResponse(code=codes.not_found_code)

        result = await existing_record.update(update_data)

        if not result:
            return APIResponse(code=codes.failed_modify_code)
        return APIResponse(success=True, code=codes.success_modify_code)

    @staticmethod
    async def crud_delete(
            queryset: Type[Document],
            data_id: str,
            codes: DefaultCodes,
    ) -> APIResponse:
        """
        向数据库删除一条记录

        Args:
            queryset: 操作的文档类
            data_id: 数据 ID
            codes: 成功代码标志, 失败代码标志, 找不到数据代码标志

        Returns:
            APIResponse: 包含操作结果的响应对象
        """
        existing_record = await queryset.get(data_id)

        if not existing_record:
            return APIResponse(code=codes.not_found_code)

        result = await existing_record.delete()

        if result.deleted_count == 0:
            return APIResponse(code=codes.failed_delete_code)
        return APIResponse(success=True, code=codes.success_delete_code)
