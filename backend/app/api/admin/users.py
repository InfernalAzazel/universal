from fastapi import APIRouter, Depends, Query, Body

from app.models.admin import User, UserQueryParams, UserCreateBody, UserEditBody
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
    '/admin/system/user',
    responses={
        200: {"model": ResponseTotalModel},
        422: {"model": ResponseModel}
    }
)
async def array(
        qp: UserQueryParams = Depends(),
        ppq: PagingQueryParams = Depends(PagingQueryParams),
        # _: UserResponseModel = Depends(auto_current_user_permission),
):
    return await User.crud_list(User, qp, ppq)


@router.post('/admin/system/user')
async def add(
        body: UserCreateBody,
        # _: UserResponseModel = Depends(auto_current_user_permission),
):
    return await User.crud_add(User, body, _codes)


@router.get('/admin/system/user/{id}')
async def retrieve(
        user_id: str = Query(..., alias='id'),
        # _: UserResponseModel = Depends(auto_current_user_permission),
):
    return await User.crud_retrieve(User, user_id, _codes)


@router.put('/admin/system/user/{id}')
async def edit(
        user_id: str = Query(..., alias='id'),
        body: UserEditBody = Body(...),
        # _: UserResponseModel = Depends(auto_current_user_permission),
):
    return await User.crud_edit(User, user_id, body, _codes)


@router.delete('/admin/system/user/{id}')
async def delete(
        user_id: str = Query(..., alias='id'),
        # _: UserResponseModel = Depends(auto_current_user_permission)
):
    return await User.crud_delete(User, user_id, _codes)
