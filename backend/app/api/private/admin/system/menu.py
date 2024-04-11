from datetime import datetime, timezone

import bson
from bson import ObjectId
from fastapi import APIRouter, Depends

from app.models.common import ResponseModel, ResponseTotalModel, PagingQueryParams
from app.models.system.menu import MenuAddOREditModel, MenuResponseModel, QueryParams
from app.models.system.role import RoleResponseModel
from app.utils.custom_response import ResponseMessages, StatusCode
from app.utils.db import pagination_query
from app.utils.dependencies import async_db_engine, get_language

router = APIRouter(
    prefix="/api",
    tags=["private admin"],
    responses={
        200: {"model": ResponseModel},
        422: {"model": ResponseModel}
    }
)


@router.get(
    '/v1/private/admin/system/menu',
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
        # _: UserResponseModel = Depends(auto_current_user_permission)
):
    coll = db_engine[MenuResponseModel.Config.name]

    try:
        qp_query = qp.to_mongo_query(exclude={'is_all_query'})
        query = {**qp_query, **ppq.to_mongo_query()}
    except bson.errors.InvalidId:
        return ResponseMessages(locale=language, status_code=StatusCode.not_valid_object_id)

    if not qp.is_all_query:
        data, total = await pagination_query(coll, query, ppq)
        data = [MenuResponseModel(**x).model_dump() for x in data]
        return ResponseMessages(locale=language, data=data, total=total)

    cursor = coll.find(qp_query)
    data = [MenuResponseModel(**x).model_dump() async for x in cursor]
    return ResponseMessages(locale=language, data=data)


@router.post('/v1/private/admin/system/menu')
async def add(
        menu_add_model: MenuAddOREditModel,
        language: str = Depends(get_language),
        db_engine=Depends(async_db_engine),
        # _: UserResponseModel = Depends(auto_current_user_permission),
):
    coll = db_engine[MenuAddOREditModel.Config.name]
    data = menu_add_model.model_dump()
    data['create_at'] = datetime.now(timezone.utc)
    count = await coll.count_documents({'key': menu_add_model.key})
    if count > 0:
        return ResponseMessages(locale=language, status_code=StatusCode.menu_add_failed)

    result = await coll.insert_one(data)
    if not result.inserted_id:
        return ResponseMessages(locale=language, status_code=StatusCode.menu_add_failed)
    return ResponseMessages(locale=language, status_code=StatusCode.menu_add_successfully, success=True)


@router.put('/v1/private/admin/system/menu')
async def edit(
        uid: str,
        menu_edit_model: MenuAddOREditModel,
        language: str = Depends(get_language),
        db_engine=Depends(async_db_engine),
        # _: UserResponseModel = Depends(auto_current_user_permission),
):
    try:
        obj_uid = ObjectId(uid)
    except bson.errors.InvalidId:
        return ResponseMessages(locale=language, status_code=StatusCode.not_valid_object_id)

    coll = db_engine[MenuAddOREditModel.Config.name]
    data = menu_edit_model.model_dump()
    data['update_at'] = datetime.utcnow()
    result = await coll.update_one(
        {'_id': obj_uid},
        {'$set': data},
    )
    if result.modified_count == 0:
        return ResponseMessages(locale=language, status_code=StatusCode.menu_modify_failed)
    return ResponseMessages(locale=language, status_code=StatusCode.menu_modify_successfully, success=True)


@router.delete('/v1/private/admin/system/menu')
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

    coll = db_engine[MenuResponseModel.Config.name]
    result = await coll.delete_one({'_id': obj_uid})
    if result.deleted_count == 0:
        return ResponseMessages(locale=language, status_code=StatusCode.menu_delete_failed)

    coll = db_engine[RoleResponseModel.Config.name]
    await coll.update_many(
        {},
        {'$pull': {
            'menu_permission': uid
        }})
    return ResponseMessages(locale=language, status_code=StatusCode.menu_delete_successfully, success=True)
