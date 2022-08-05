from datetime import datetime

import pymongo
import pytz
from bson import ObjectId
from fastapi import APIRouter, Depends, status, Query
from fastapi.encoders import jsonable_encoder
from pymongo import ReturnDocument
from starlette.responses import JSONResponse

from app.utils.cfg import Config
from app.utils.custom_http_exception import CustomHttpException as http_exp
from app.utils.dependencies import get_config, get_db_client_c, auto_current_user_permission
from app.utils.menu_node_tree import list_to_tree
from app.models.system.menu import Menu, SearchMenu
from app.models.system.users import User
from app.settings import DATABASE_NAME, COLL_MENU, COLL_ROLE

router = APIRouter(
    prefix="/api",
    tags=["system"],
)


@router.get('/v1/system/menu/all')
async def all(
        cfg: Config = Depends(get_config),
        current_user: User = Depends(auto_current_user_permission),
):
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_MENU]

    query = {}

    cursor = coll.find(query).sort([
        ('order', pymongo.ASCENDING),
    ])

    try:
        menu_list = [Menu(**x) async for x in cursor]
        data = list_to_tree(jsonable_encoder(menu_list), 0)
    except Exception as _:
        print(_)
        data = []
    db_client.close()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(data)
    )


@router.get('/v1/system/menu/list')
async def lists(
        id: str = None,
        key: int = None,
        father: int = None,
        hide: bool = None,
        path: str = None,
        title_zh_cn: str = None,
        title_en_us: str = None,
        icon: str = None,
        component: str = None,
        order: int = None,
        create_at: list[datetime] = Query(None),
        update_at: list[datetime] = Query(None),
        current_page: int = 1,  # 跳过
        page_size: int = 10,  # 跳过
        cfg: Config = Depends(get_config),
        current_user: User = Depends(auto_current_user_permission)
):
    skip = (current_page - 1) * page_size
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_MENU]
    search_menu = SearchMenu(
        key=key,
        father=father,
        hide=hide,
        path=path,
        title_zh_cn=title_zh_cn,
        title_en_us=title_en_us,
        icon=icon,
        component=component,
        order=order,
    )
    query = search_menu.dict(exclude_none=True)

    if id is not None and id != '':
        query['_id'] = ObjectId(id)
    if update_at:
        query['update_at'] = {'$gte': update_at[0].astimezone(pytz.utc), '$lte': update_at[1].astimezone(pytz.utc)}
    if create_at:
        query['create_at'] = {'$gte': create_at[0].astimezone(pytz.utc), '$lte': create_at[1].astimezone(pytz.utc)}

    cursor = coll.find(query).skip(skip).limit(page_size).sort([
        ('order', pymongo.ASCENDING),
    ])
    count = await coll.count_documents(query)
    try:
        menu_list = [Menu(**x) async for x in cursor]
        data = list_to_tree(jsonable_encoder(menu_list), 0)
    except Exception as _:
        print(_)
        data = []
    db_client.close()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({'data': data, 'total': count})
    )


@router.post('/v1/system/menu/add')
async def add(
        menu: Menu,
        cfg: Config = Depends(get_config),
        current_user: User = Depends(auto_current_user_permission),
):
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_MENU]
    doc = await coll.find_one({'key': menu.key})
    if doc:
        raise http_exp.client_err_role_key_already_exists()
    menu.create_at = datetime.now(pytz.utc)
    await coll.find_one_and_update(
        {'key': menu.key},
        {'$set': menu.dict()},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    db_client.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'menu added ok'}
    )


@router.put('/v1/system/menu/edit')
async def edit(
        menu: Menu,
        cfg: Config = Depends(get_config),
   current_user: User = Depends(auto_current_user_permission),
):
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_MENU]
    menu.update_at = datetime.now(pytz.utc)
    await coll.find_one_and_update(
        {'_id': ObjectId(menu.id)},
        # 前端会自带 id create_at children 字段，所以这里不需要更新
        {'$set': menu.dict(exclude={'id', 'create_at', 'children'})},
    )
    db_client.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'menu edit ok'}
    )


@router.delete('/v1/system/menu/delete')
async def delete(
        id: str,
        cfg: Config = Depends(get_config),
        current_user: User = Depends(auto_current_user_permission),
):
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_ROLE]
    await coll.update_many(
        {},
        {'$pull': {
            'menu_permission': {'id': id}
        }})
    coll = db_client[DATABASE_NAME][COLL_MENU]
    await coll.delete_one({'_id': ObjectId(id)})
    db_client.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'menu delete ok'}
    )
