from datetime import datetime, timezone

import bson
from bson import ObjectId
from fastapi import APIRouter, Depends

from app.models.common import ResponseTotalModel, ResponseModel, PagingQueryParams
from app.models.system.interface import InterfaceAddOREditModel, InterfaceResponseModel, QueryParams
from app.models.system.role import RoleResponseModel
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
    '/v1/private/admin/system/interface',
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
    coll = db_engine[InterfaceResponseModel.Config.name]

    try:
        qp_query = qp.to_mongo_query(exclude={'is_all_query'})
        query = {**qp_query, **ppq.to_mongo_query()}
    except bson.errors.InvalidId:
        return ResponseMessages(locale=language, status_code=StatusCode.not_valid_object_id)

    if not qp.is_all_query:
        data, total = await pagination_query(coll, query, ppq)
        data = [InterfaceResponseModel(**x).model_dump() for x in data]
        return ResponseMessages(locale=language, data=data, total=total)

    cursor = coll.find(qp_query)
    data = [InterfaceResponseModel(**x).model_dump() async for x in cursor]
    return ResponseMessages(locale=language, data=data)


@router.post('/v1/private/admin/system/interface')
async def add(
        interface_add_model: InterfaceAddOREditModel,
        language: str = Depends(get_language),
        db_engine=Depends(async_db_engine),
        # _: UserResponseModel = Depends(auto_current_user_permission),
):
    coll = db_engine[interface_add_model.Config.name]
    data = interface_add_model.model_dump()
    data['create_at'] = datetime.now(timezone.utc)

    result = await coll.insert_one(data)
    if not result.inserted_id:
        return ResponseMessages(locale=language, status_code=StatusCode.interface_add_failed)
    return ResponseMessages(locale=language, status_code=StatusCode.interface_add_successfully, success=True)


@router.put('/v1/private/admin/system/interface')
async def edit(
        uid: str,
        interface_edit_model: InterfaceAddOREditModel,
        language: str = Depends(get_language),
        db_engine=Depends(async_db_engine),
        # _: UserResponseModel = Depends(auto_current_user_permission),
):
    try:
        obj_uid = ObjectId(uid)
    except bson.errors.InvalidId:
        return ResponseMessages(locale=language, status_code=StatusCode.not_valid_object_id)

    coll = db_engine[interface_edit_model.Config.name]
    data = interface_edit_model.model_dump()
    data['update_at'] = datetime.now(timezone.utc)
    result = await coll.update_one(
        {'_id': obj_uid},
        {'$set': data},
    )
    if result.modified_count == 0:
        return ResponseMessages(locale=language, status_code=StatusCode.interface_modify_failed)
    return ResponseMessages(locale=language, status_code=StatusCode.interface_modify_successfully, success=True)


@router.delete('/v1/private/admin/system/interface')
async def delete(
        uid: str,
        language: str = Depends(get_language),
        db_engine=Depends(async_db_engine),
        # _: UserResponseModel = Depends(auto_current_user_permission)
):
    try:
        obj_uid = ObjectId(uid)
    except bson.errors.InvalidId:
        return ResponseMessages(locale=language, status_code=StatusCode.not_valid_object_id)

    coll = db_engine[RoleResponseModel.Config.name]
    await coll.update_many(
        {},
        {'$pull': {
            'interface_permission': uid
        }})
    coll = db_engine[InterfaceAddOREditModel.Config.name]
    result = await coll.delete_one({'_id': obj_uid})
    if result.deleted_count == 0:
        return ResponseMessages(locale=language, status_code=StatusCode.interface_delete_failed)
    return ResponseMessages(locale=language, status_code=StatusCode.interface_delete_successfully, success=True)
