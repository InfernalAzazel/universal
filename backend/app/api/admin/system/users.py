from fastapi import APIRouter, Depends, Query, Body

from app.models.admin import User, UserQueryParams, UserCreateBody, UserEditBody
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
    success_retrieve_code=StatusCode.user_retrieve_successfully.value,
    success_add_code=StatusCode.user_add_successfully.value,
    success_modify_code=StatusCode.user_modify_successfully.value,
    success_delete_code=StatusCode.user_delete_successfully.value,
    failed_retrieve_code=StatusCode.user_retrieve_failed.value,
    failed_add_code=StatusCode.user_add_failed.value,
    failed_modify_code=StatusCode.user_modify_successfully.value,
    failed_delete_code=StatusCode.user_delete_successfully.value,
    not_found_code=StatusCode.user_not_found.value
)


@router.get(
    '/admin/system/users',
    responses={
        200: {"model": ResponseTotalModel},
        422: {"model": ResponseModel}
    }
)
async def array(
        qp: UserQueryParams = Depends(),
        ppq: PagingQueryParams = Depends(PagingQueryParams),
        _: User = Depends(auto_current_user_permission),
):
    return await User.crud_list(User, qp, ppq)


@router.post('/admin/system/users')
async def add(
        body: UserCreateBody,
        _: User = Depends(auto_current_user_permission),
):
    return await User.crud_add(User, body, _codes)


@router.get('/admin/system/users/{id}')
async def retrieve(
        user_id: str = Query(..., alias='id'),
        _: User = Depends(auto_current_user_permission),
):
    return await User.crud_retrieve(User, user_id, _codes)


@router.put('/admin/system/users/{id}')
async def edit(
        user_id: str = Query(..., alias='id'),
        body: UserEditBody = Body(...),
        current_user: User = Depends(auto_current_user_permission),
):
    user = await User.get(user_id)
    if not user:
        return APIResponse(success=False, code=_codes.not_found_code)

    # 只要超级管理员才能编辑超级管理员
    if not current_user.is_super and user.is_super:
        return APIResponse(success=False, code=StatusCode.user_modify_admin_failed.value)

    return await User.crud_edit(User, user_id, body, _codes)


@router.delete('/admin/system/users/{id}')
async def delete(
        user_id: str = Query(..., alias='id'),
        _: User = Depends(auto_current_user_permission),
):
    existing_record = await User.get(user_id)

    if not existing_record:
        return APIResponse(code=_codes.not_found_code)

    # 不允许删除超级管理员
    if existing_record.is_super:
        return APIResponse(code=StatusCode.user_delete_admin_failed.value)

    return await User.crud_delete(User, user_id, _codes)
