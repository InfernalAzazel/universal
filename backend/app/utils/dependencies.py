from typing import Optional

import casbin
from bunnet.operators import In
from bson import ObjectId
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError
from jose.exceptions import JWTClaimsError, JWTError

from app.models.admin import User, Role, Interface
from app.utils.api_response import ExceptionResponse, StatusCode
from app.utils.casbin_adapter import Adapter
from app.utils.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


def get_language(request: Request):
    language = request.headers.get("Customize-Language", "en_us")
    return language


# 获取当前用户
def get_current_user(
        token: str = Depends(oauth2_scheme),
):
    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise ExceptionResponse(code=StatusCode.jwt_decode_failed.value)
    except ExpiredSignatureError as _:
        raise ExceptionResponse(code=StatusCode.jwt_expired.value)
    except JWTClaimsError as _:
        raise ExceptionResponse(code=StatusCode.jwt_decode_failed.value)
    except JWTError as _:
        raise ExceptionResponse(code=StatusCode.jwt_decode_failed.value)

    user: Optional[User] = ~User.find_one(User.username == username)

    if user is None:
        raise ExceptionResponse(code=StatusCode.credentials_invalid.value)
    return user


# 自动用户认证权限
async def auto_current_user_permission(
        request: Request,
        current_user: User = Depends(get_current_user)
):
    path = request.url.path
    method = request.method

    interface_permission = []

    if current_user.disabled:
        raise ExceptionResponse(code=StatusCode.user_disabled.value)

    roles = Role.find(In(Role.title, current_user.role_names)).to_list()

    # 添加多个角色接口权限
    for role in roles:
        interface_permission.extend(role.interface_permission)

    # 获取角色失败
    if not interface_permission:
        raise ExceptionResponse(code=StatusCode.get_roles_failed.value)
    # 多角色接口权限 -> 去重
    interface_permission = list(set(interface_permission))

    # 获取接口
    obj_uids = [ObjectId(uid) for uid in interface_permission]
    interfaces = Interface.find({'_id': {'$in': obj_uids}}).to_list()

    # 设置适配器
    adapter = Adapter(roles, interfaces)
    e = casbin.Enforcer('rbac_model.conf', adapter)
    role_ids = '|'.join([str(role.id) for role in roles])

    # 验证接口权限
    if e.enforce(role_ids, path, method):
        pass
    else:
        # 非法登录
        if path == '/api/v1/root/info/routes':
            raise ExceptionResponse(code=StatusCode.illegal_login.value)
        raise ExceptionResponse(code=StatusCode.unauthorized.value)
    return current_user
