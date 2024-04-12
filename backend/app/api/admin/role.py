from fastapi import APIRouter, Depends, Query, Body

from app.models.admin import Role, RoleQueryParams, RoleCreateBody, RoleEditBody
from app.models.common import ResponseTotalModel, ResponseModel, PagingQueryParams
from app.utils.api_response import StatusCode, DefaultCodes

router = APIRouter(
    prefix="/api/v1",
    tags=["private admin"],
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
async def array(
        qp: RoleQueryParams = Depends(),
        ppq: PagingQueryParams = Depends(PagingQueryParams),
        # _: UserResponseModel = Depends(auto_current_user_permission),
):
    return await Role.crud_list(Role, qp, ppq)


@router.post('/admin/system/role')
async def add(
        body: RoleCreateBody,
        # _: UserResponseModel = Depends(auto_current_user_permission),
):
    return await Role.crud_add(Role, body, _codes)


@router.get('/admin/system/role/{id}')
async def retrieve(
        role_id: str = Query(..., alias='id'),
        # _: UserResponseModel = Depends(auto_current_user_permission),
):
    return await Role.crud_retrieve(Role, role_id, _codes)


@router.put('/admin/system/role/{id}')
async def edit(
        role_id: str = Query(..., alias='id'),
        body: RoleEditBody = Body(...),
        # _: UserResponseModel = Depends(auto_current_user_permission),
):
    return await Role.crud_edit(Role, role_id, body, _codes)


@router.delete('/admin/system/role/{id}')
async def delete(
        role_id: str = Query(..., alias='id'),
        # _: UserResponseModel = Depends(auto_current_user_permission)
):
    return await Role.crud_delete(Role, role_id, _codes)
