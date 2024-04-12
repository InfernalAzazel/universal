from fastapi import APIRouter, Depends, Query, Body

from app.models.admin import Menu, MenuQueryParams, MenuCreateBody, MenuEditBody
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
async def array(
        qp: MenuQueryParams = Depends(),
        ppq: PagingQueryParams = Depends(PagingQueryParams),
        # _: UserResponseModel = Depends(auto_current_user_permission),
):
    return await Menu.crud_list(Menu, qp, ppq)


@router.post('/admin/system/menu')
async def add(
        body: MenuCreateBody,
        # _: UserResponseModel = Depends(auto_current_user_permission),
):
    return await Menu.crud_add(Menu, body, _codes)


@router.get('/admin/system/menu/{id}')
async def retrieve(
        menu_id: str = Query(..., alias='id'),
        # _: UserResponseModel = Depends(auto_current_user_permission),
):
    return await Menu.crud_retrieve(Menu, menu_id, _codes)


@router.put('/admin/system/menu/{id}')
async def edit(
        menu_id: str = Query(..., alias='id'),
        body: MenuEditBody = Body(...),
        # _: UserResponseModel = Depends(auto_current_user_permission),
):
    return await Menu.crud_edit(Menu, menu_id, body, _codes)


@router.delete('/admin/system/menu/{id}')
async def delete(
        menu_id: str = Query(..., alias='id'),
        # _: UserResponseModel = Depends(auto_current_user_permission)
):
    return await Menu.crud_delete(Menu, menu_id, _codes)
