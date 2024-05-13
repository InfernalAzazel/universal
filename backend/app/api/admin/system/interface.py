from fastapi import APIRouter, Depends, Query, Body

from app.models.admin import Interface, User
from app.models.admin_dtos import InterfaceQueryParams, InterfaceCreateBody, InterfaceEditBody
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
def array(
        qp: InterfaceQueryParams = Depends(),
        ppq: PagingQueryParams = Depends(PagingQueryParams),
        _: User = Depends(auto_current_user_permission),
):
    return Interface.crud_list(qp, ppq)


@router.post('/admin/system/interface')
def add(
        body: InterfaceCreateBody,
        _: User = Depends(auto_current_user_permission),
):
    return Interface.crud_add(body, _codes)


@router.get('/admin/system/interface/{id}')
def retrieve(
        interface_id: str = Query(..., alias='id'),
        _: User = Depends(auto_current_user_permission),
):
    return Interface.crud_retrieve(interface_id, _codes)


@router.put('/admin/system/interface/{id}')
def edit(
        interface_id: str = Query(..., alias='id'),
        body: InterfaceEditBody = Body(...),
        _: User = Depends(auto_current_user_permission),
):
    return Interface.crud_edit(interface_id, body, _codes)


@router.delete('/admin/system/interface/{id}')
def delete(
        interface_id: str = Query(..., alias='id'),
        _: User = Depends(auto_current_user_permission)
):
    return Interface.crud_delete(interface_id, _codes)
