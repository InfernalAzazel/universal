from datetime import datetime
from datetime import timezone

import bson
from bson import ObjectId
from fastapi import APIRouter, Depends

from app.models.common import ResponseModel, ResponseTotalModel, PagingQueryParams
from app.models.system.user import QueryParams, UserResponseModel, UserAddModel, UserEditModel
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
    '/v1/private/admin/system/users',
    responses={
        200: {"model": ResponseTotalModel},
        422: {"model": ResponseModel}
    }
)
async def array(
        qp: QueryParams = Depends(),
        ppq: PagingQueryParams = Depends(PagingQueryParams),
        language: str = Depends(get_language),
        db_engine=Depends(async_db_engine),
        # _: UserResponseModel = Depends(auto_current_user_permission)

):
    coll = db_engine[UserResponseModel.Config.name]
    try:
        qp_query = qp.to_mongo_query()
        query = {**qp_query, **ppq.to_mongo_query()}
    except bson.errors.InvalidId:
        return ResponseMessages(locale=language, status_code=StatusCode.not_valid_object_id)

    data, total = await pagination_query(coll, query, ppq)
    data = [UserResponseModel(**x).model_dump() for x in data]
    return ResponseMessages(locale=language, data=data, total=total)


@router.post('/v1/private/admin/system/users')
async def add(
        user_add_model: UserAddModel,
        language: str = Depends(get_language),
        db_engine=Depends(async_db_engine),
        # _: UserResponseModel = Depends(auto_current_user_permission)
):
    coll = db_engine[UserResponseModel.Config.name]
    doc = await coll.find_one({'username': user_add_model.username})

    if doc:
        return ResponseMessages(locale=language, status_code=StatusCode.user_add_failed)

    data = user_add_model.model_dump()
    data['create_at'] = datetime.now(timezone.utc)
    result = await coll.insert_one(data)

    if not result.inserted_id:
        return ResponseMessages(locale=language, status_code=StatusCode.user_add_failed)
    return ResponseMessages(locale=language, status_code=StatusCode.user_add_successfully, success=True)


@router.put('/v1/private/admin/system/users')
async def edit(
        uid: str,
        user_edit_model: UserEditModel,
        language: str = Depends(get_language),
        db_engine=Depends(async_db_engine),
        # _: UserResponseModel = Depends(auto_current_user_permission),
):
    try:
        obj_uid = ObjectId(uid)
    except bson.errors.InvalidId:
        return ResponseMessages(locale=language, status_code=StatusCode.not_valid_object_id)

    coll = db_engine[UserResponseModel.Config.name]
    data = user_edit_model.model_dump()
    data['update_at'] = datetime.utcnow()

    result = await coll.update_one(
        {'_id': obj_uid},
        {'$set': data},
    )
    if result.modified_count == 0:
        return ResponseMessages(locale=language, status_code=StatusCode.user_modify_failed)
    return ResponseMessages(locale=language, status_code=StatusCode.user_modify_successfully, success=True)


@router.delete('/v1/private/admin/system/users')
async def delete(
        uid: str,
        language: str = Depends(get_language),
        db_engine=Depends(async_db_engine),
        # _: UserResponseModel = Depends(auto_current_user_permission),
):
    try:
        obj_uid = ObjectId(uid)
    except bson.errors.InvalidId:
        return ResponseMessages(locale=language, status_code=StatusCode.not_valid_object_id)

    coll = db_engine[UserResponseModel.Config.name]
    result = await coll.delete_one({'_id': obj_uid})
    if result.deleted_count == 0:
        return ResponseMessages(locale=language, status_code=StatusCode.user_delete_failed)
    return ResponseMessages(locale=language, status_code=StatusCode.user_delete_successfully, success=True)
