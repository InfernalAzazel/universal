from typing import Optional

from fastapi import APIRouter, Depends, Query, Body

from app.models.admin import Role, User
from app.models.admin_dtos import RoleQueryParams, RoleCreateBody, RoleEditBody
from app.models.common import ResponseTotalModel, ResponseModel, PagingQueryParams
from app.utils.api_response import StatusCode, DefaultCodes, APIResponse
from app.utils.dependencies import auto_current_user_permission

router = APIRouter(
    prefix="/api/v1",
    tags=["admin"],
    responses={
        200: {"model": ResponseModel},
        422: {"model": ResponseModel}
    }
)

_codes = DefaultCodes(
    success_retrieve_code=StatusCode.role_retrieve_successfully.value,
    success_add_code=StatusCode.role_add_successfully.value,
    success_modify_code=StatusCode.role_modify_successfully.value,
    success_delete_code=StatusCode.role_delete_successfully.value,
    failed_retrieve_code=StatusCode.role_retrieve_failed.value,
    failed_add_code=StatusCode.role_add_failed.value,
    failed_modify_code=StatusCode.role_modify_successfully.value,
    failed_delete_code=StatusCode.role_delete_successfully.value,
    not_found_code=StatusCode.role_not_found.value
)


@router.get(
    '/admin/system/role',
    responses={
        200: {"model": ResponseTotalModel},
        422: {"model": ResponseModel}
    }
)
def array(
        qp: RoleQueryParams = Depends(),
        ppq: PagingQueryParams = Depends(PagingQueryParams),
        _: User = Depends(auto_current_user_permission),
):
    return Role.crud_list(qp, ppq)


@router.post('/admin/system/role')
def add(
        body: RoleCreateBody,
        _: User = Depends(auto_current_user_permission),
):
    return Role.crud_add(body, _codes)


@router.get('/admin/system/role/{id}')
def retrieve(
        role_id: str = Query(..., alias='id'),
        _: User = Depends(auto_current_user_permission),
):
    return Role.crud_retrieve(role_id, _codes)


@router.put('/admin/system/role/{id}')
def edit(
        role_id: str = Query(..., alias='id'),
        body: RoleEditBody = Body(...),
        current_user: User = Depends(auto_current_user_permission),
):
    role: Optional[Role] = ~Role.get(role_id)
    if not role:
        return APIResponse(success=False, code=_codes.not_found_code)

    # 只要超级管理员才能编辑超级管理员 角色
    if not current_user.is_super and role.is_super:
        return APIResponse(success=False, code=StatusCode.role_modify_admin_failed.value)

    # 更新用户的角色名称
    User.find({"role_names": role.title}).update(
        {"$set": {"role_names.$[elem]": body.title}},
        array_filters=[{"elem": role.title}]
    ).run()
    return Role.crud_edit(role_id, body, _codes)


@router.delete('/admin/system/role/{id}')
def delete(
        role_id: str = Query(..., alias='id'),
        _: User = Depends(auto_current_user_permission),
):
    role: Optional[Role] = ~Role.get(role_id)

    if not role:
        return APIResponse(code=_codes.not_found_code)

    # 不允许删除超级管理员 角色
    if role.is_super:
        return APIResponse(code=StatusCode.role_delete_admin_failed.value)

    # 删除相关用户角色
    User.find({"role_names": role.title}).update(
        {"$pull": {"role_names": role.title}}
    ).run()
    return Role.crud_delete(role_id, _codes)
