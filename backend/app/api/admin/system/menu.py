from fastapi import APIRouter, Depends, Query, Body

from app.models.admin import Menu, User
from app.models.admin_dtos import MenuQueryParams, MenuCreateBody, MenuEditBody
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
    success_retrieve_code=StatusCode.menu_retrieve_successfully.value,
    success_add_code=StatusCode.menu_add_successfully.value,
    success_modify_code=StatusCode.menu_modify_successfully.value,
    success_delete_code=StatusCode.menu_delete_successfully.value,
    failed_retrieve_code=StatusCode.menu_retrieve_failed.value,
    failed_add_code=StatusCode.menu_add_failed.value,
    failed_modify_code=StatusCode.menu_modify_successfully.value,
    failed_delete_code=StatusCode.menu_delete_successfully.value,
    not_found_code=StatusCode.menu_not_found.value
)


@router.get(
    '/admin/system/menu',
    responses={
        200: {"model": ResponseTotalModel},
        422: {"model": ResponseModel}
    }
)
def array(
        qp: MenuQueryParams = Depends(),
        ppq: PagingQueryParams = Depends(PagingQueryParams),
        _: User = Depends(auto_current_user_permission),
):
    return Menu.crud_list(qp, ppq)


@router.post('/admin/system/menu')
def add(
        body: MenuCreateBody,
        _: User = Depends(auto_current_user_permission),
):
    return Menu.crud_add(body, _codes)


@router.get('/admin/system/menu/{id}')
def retrieve(
        menu_id: str = Query(..., alias='id'),
        _: User = Depends(auto_current_user_permission),
):
    return Menu.crud_retrieve(menu_id, _codes)


@router.put('/admin/system/menu/{id}')
def edit(
        menu_id: str = Query(..., alias='id'),
        body: MenuEditBody = Body(...),
        _: User = Depends(auto_current_user_permission),
):
    return Menu.crud_edit(menu_id, body, _codes)


@router.delete('/admin/system/menu/{id}')
def delete(
        menu_id: str = Query(..., alias='id'),
        _: User = Depends(auto_current_user_permission)
):
    return Menu.crud_delete(menu_id, _codes)
