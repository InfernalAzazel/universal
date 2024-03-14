from datetime import datetime, timezone
import bson
from bson import ObjectId
from fastapi import APIRouter, Depends
from app.models.common import ResponseModel, ResponseTotalModel, PagingQueryParams
from app.models.system.role import RoleResponseModel, RoleAddOREditModel, QueryParams
from app.models.system.user import UserResponseModel
from app.utils.custom_response import ResponseMessages, StatusCode
from app.utils.db import async_db_engine, pagination_query
from app.utils.dependencies import get_language

router = APIRouter(
    prefix="/api",
    tags=["private admin"],
    responses={
        200: {"model": ResponseModel},
        422: {"model": ResponseModel}
    }
)


@router.get(
    '/v1/private/admin/system/role',
    responses={
        200: {"model": ResponseTotalModel},
        422: {"model": ResponseModel}
    }
)
async def array(
        qp: QueryParams = Depends(QueryParams),
        ppq: PagingQueryParams = Depends(PagingQueryParams),
        language: str = Depends(get_language),
        db_engine=Depends(async_db_engine),
        # _: UserResponseModel = Depends(auto_current_user_permission),
):
    coll = db_engine[RoleResponseModel.Config.name]

    try:
        qp_query = qp.to_mongo_query(exclude={'is_all_query'})
        query = {**qp_query, **ppq.to_mongo_query()}
    except bson.errors.InvalidId:
        return ResponseMessages(locale=language, status_code=StatusCode.not_valid_object_id)

    if not qp.is_all_query:
        data, total = await pagination_query(coll, query, ppq)
        data = [RoleResponseModel(**x).model_dump() for x in data]
        return ResponseMessages(locale=language, data=data, total=total)

    cursor = coll.find(qp_query)
    data = [RoleResponseModel(**x).model_dump() async for x in cursor]
    return ResponseMessages(locale=language, data=data)


@router.post('/v1/private/admin/system/role')
async def add(
        role_add_model: RoleAddOREditModel,
        language: str = Depends(get_language),
        db_engine=Depends(async_db_engine),
        # _: UserResponseModel = Depends(auto_current_user_permission),
):
    coll = db_engine[role_add_model.Config.name]
    count = await coll.count_documents({'title': role_add_model.title})
    role_add_model.menu_permission = []
    role_add_model.interface_permission = []
    data = role_add_model.model_dump()
    data['create_at'] = datetime.now(timezone.utc)
    if count > 0:
        return ResponseMessages(locale=language, status_code=StatusCode.role_add_failed)

    result = await coll.insert_one(data)
    if not result.inserted_id:
        return ResponseMessages(locale=language, status_code=StatusCode.role_add_failed)
    return ResponseMessages(locale=language, status_code=StatusCode.role_add_successfully, success=True)


@router.put('/v1/private/admin/system/role')
async def edit(
        uid: str,
        role_edit_model: RoleAddOREditModel,
        language: str = Depends(get_language),
        db_engine=Depends(async_db_engine),
        # _: UserResponseModel = Depends(auto_current_user_permission),
):
    try:
        obj_uid = ObjectId(uid)
    except bson.errors.InvalidId:
        return ResponseMessages(locale=language, status_code=StatusCode.not_valid_object_id)

    coll = db_engine[role_edit_model.Config.name]
    data = role_edit_model.model_dump(exclude_none=True)
    data['update_at'] = datetime.utcnow()
    # 修改角色并且返回修改前的文档
    result = await coll.find_one_and_update(
        {'_id': obj_uid},
        {'$set': data},
    )

    if result is None or not result:
        return ResponseMessages(locale=language, status_code=StatusCode.role_modify_failed)
    old_role_model = RoleResponseModel(**result)

    # 更新用户的角色名称
    coll = db_engine[UserResponseModel.Config.name]
    await coll.update_many(
        {'role_names': old_role_model.title},
        {"$set": {"role_names.$[elem]": role_edit_model.title}},
        array_filters=[{"elem": old_role_model.title}]
    )

    return ResponseMessages(locale=language, status_code=StatusCode.role_modify_successfully, success=True)


@router.delete('/v1/private/admin/system/role')
async def delete(
        uid: str,
        language: str = Depends(get_language),
        db_engine=Depends(async_db_engine),
        # _: UserResponseModel = Depends(auto_current_user_permission),
):
    coll = db_engine[RoleResponseModel.Config.name]
    try:
        obj_uid = ObjectId(uid)
    except bson.errors.InvalidId:
        return ResponseMessages(locale=language, status_code=StatusCode.not_valid_object_id)

    old_document = await coll.find_one_and_delete({'_id': obj_uid})
    if not old_document:
        return ResponseMessages(locale=language, status_code=StatusCode.menu_delete_failed)

    old_role_model = RoleResponseModel(**old_document)

    coll = db_engine[UserResponseModel.Config.name]

    await coll.update_many(
        {"role_names": old_role_model.title},
        {"$pull": {"role_names": old_role_model.title}}
    )

    return ResponseMessages(locale=language, status_code=StatusCode.role_delete_successfully, success=True)
