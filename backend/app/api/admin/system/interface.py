from fastapi import APIRouter, Depends, Query, Body

from app.models.admin import Interface, InterfaceQueryParams, InterfaceCreateBody, InterfaceEditBody, User
from app.models.common import ResponseTotalModel, ResponseModel, PagingQueryParams
from app.utils.api_response import StatusCode, DefaultCodes
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
    success_retrieve_code=StatusCode.interface_retrieve_successfully.value,
    success_add_code=StatusCode.interface_add_successfully.value,
    success_modify_code=StatusCode.interface_modify_successfully.value,
    success_delete_code=StatusCode.interface_delete_successfully.value,
    failed_retrieve_code=StatusCode.interface_retrieve_failed.value,
    failed_add_code=StatusCode.interface_add_failed.value,
    failed_modify_code=StatusCode.interface_modify_successfully.value,
    failed_delete_code=StatusCode.interface_delete_successfully.value,
    not_found_code=StatusCode.interface_not_found.value
)


@router.get(
    '/admin/system/interface',
    responses={
        200: {"model": ResponseTotalModel},
        422: {"model": ResponseModel}
    }
)
async def array(
        qp: InterfaceQueryParams = Depends(),
        ppq: PagingQueryParams = Depends(PagingQueryParams),
        _: User = Depends(auto_current_user_permission),
):
    return await Interface.crud_list(Interface, qp, ppq)


@router.post('/admin/system/interface')
async def add(
        body: InterfaceCreateBody,
        _: User = Depends(auto_current_user_permission),
):
    return await Interface.crud_add(Interface, body, _codes)


@router.get('/admin/system/interface/{id}')
async def retrieve(
        interface_id: str = Query(..., alias='id'),
        _: User = Depends(auto_current_user_permission),
):
    return await Interface.crud_retrieve(Interface, interface_id, _codes)


@router.put('/admin/system/interface/{id}')
async def edit(
        interface_id: str = Query(..., alias='id'),
        body: InterfaceEditBody = Body(...),
        _: User = Depends(auto_current_user_permission),
):
    return await Interface.crud_edit(Interface, interface_id, body, _codes)


@router.delete('/admin/system/interface/{id}')
async def delete(
        interface_id: str = Query(..., alias='id'),
        _: User = Depends(auto_current_user_permission)
):
    return await Interface.crud_delete(Interface, interface_id, _codes)
