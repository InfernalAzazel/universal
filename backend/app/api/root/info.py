import bson
from bunnet.operators import In
from bson import ObjectId
from fastapi import APIRouter, Depends

from app.models.admin import Role, Menu, User
from app.models.common import ResponseModel
from app.utils.api_response import APIResponse, StatusCode
from app.utils.dependencies import auto_current_user_permission

router = APIRouter(
    prefix="/api/v1",
    tags=["root"],
    responses={
        200: {"model": ResponseModel},
        422: {"model": ResponseModel}
    }
)


@router.get('/root/info/account')
def account(
        current_user: User = Depends(auto_current_user_permission),
):
    return APIResponse(data=current_user)


@router.get('/root/info/routes')
def routers(
        current_user: User = Depends(auto_current_user_permission)
):
    # 获取当前用户的角色
    roles = Role.find(In(Role.title, current_user.role_names)).to_list()

    # 获取角色关联的菜单权限
    menu_permissions = []
    for role in roles:
        menu_permissions.extend(role.menu_permission)

    if not menu_permissions:
        return APIResponse(code=StatusCode.role_not_found.value)

    # 去重
    unique_menu_permissions = list(set(menu_permissions))

    try:
        obj_uids = [ObjectId(uid) for uid in unique_menu_permissions]
    except bson.errors.InvalidId:
        return APIResponse(code=StatusCode.not_valid_object_id.value)

    # 根据菜单权限获取菜单详情
    menus = Menu.find(In(Menu.id, obj_uids)).to_list()

    if not menus:
        return APIResponse(code=StatusCode.illegal_login.value)

    return APIResponse(menus)