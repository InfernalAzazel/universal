import bson
import httpx
from bson import ObjectId
from fastapi import APIRouter, Depends
from app.models.common import ResponseModel
from app.models.system.menu import MenuResponseModel
from app.models.system.role import RoleResponseModel
from app.models.system.user import UserResponseModel
from app.utils.custom_response import ResponseMessages, StatusCode
from app.utils.db import async_db_engine
from app.utils.dependencies import auto_current_user_permission, get_language

router = APIRouter(
    prefix="/api",
    tags=["private root"],
    responses={
        200: {"model": ResponseModel},
        422: {"model": ResponseModel}
    }
)


@router.get('/v1/private/root/info/account')
async def account(
        language: str = Depends(get_language),
        current_user: UserResponseModel = Depends(auto_current_user_permission),
):
    return ResponseMessages(locale=language, data=current_user)


@router.get('/v1/private/root/info/routes')
async def routers(
        language: str = Depends(get_language),
        current_user: UserResponseModel = Depends(auto_current_user_permission),
        db_engine=Depends(async_db_engine)
):
    # 角色
    coll = db_engine[RoleResponseModel.Config.name]

    cursor = coll.find({'title': {'$in': current_user.role_names}})
    menu_permission = []
    # 添加多个角色菜单权限
    async for x in cursor:
        role_model = RoleResponseModel(**x)
        menu_permission.extend(role_model.menu_permission)

    if not menu_permission:
        ResponseMessages(locale=language, status_code=StatusCode.role_get_failed)
    # 去重
    menu_permission = list(set(menu_permission))

    try:
        obj_uids = [ObjectId(uid) for uid in menu_permission]
    except bson.errors.InvalidId:
        return ResponseMessages(locale=language, status_code=StatusCode.not_valid_object_id)

    query = {'_id': {'$in': obj_uids}}
    # 菜单
    coll = db_engine[MenuResponseModel.Config.name]
    cursor = coll.find(query)
    data = [MenuResponseModel(**x).model_dump() async for x in cursor]
    # 没有分配菜单权限非法登录
    if not data:
        return ResponseMessages(locale=language, status_code=StatusCode.illegal_login)
    return ResponseMessages(locale=language, data=data)
