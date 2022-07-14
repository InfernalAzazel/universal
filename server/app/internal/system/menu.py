from typing import Any, TYPE_CHECKING

from bson import ObjectId
from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pymongo import ReturnDocument
from starlette.responses import JSONResponse

from app.cfg import Config
from app.custom_http_exception import CustomHttpException as http_exp
from app.dependencies import get_config, get_db_client_c
from app.menu_node_tree import list_to_tree
from app.settings import DATABASE_NAME, COLL_MENU

router = APIRouter(
    prefix="/api",
    tags=["system"],
)


class Menu(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)
        for k, v in data.items():
            if k == '_id':
                self.__dict__['id'] = str(data['_id'])
            else:
                self.__dict__[k] = data[k]

    if TYPE_CHECKING:
        id: str = None
    key: int
    father: int
    hide: bool
    path: str
    title: str
    icon: str
    component: str


class SearchMenu(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)
        for k, v in data.items():
            if k == '_id' and v == '':
                self.__dict__['id'] = None
            if k == 'key' and v == '':
                self.__dict__['key'] = None
            elif k == 'father' and v == '':
                self.__dict__['father'] = None
            elif k == 'hide' and v == '':
                self.__dict__['hide'] = None
            elif k == 'path' and v == '':
                self.__dict__['path'] = None
            elif k == 'title' and v == '':
                self.__dict__['title'] = None
            elif k == 'icon' and v == '':
                self.__dict__['icon'] = None
            elif k == 'component' and v == '':
                self.__dict__['component'] = None
            else:
                self.__dict__[k] = data[k]

    if TYPE_CHECKING:
        id: str = None
    key: int = None
    father: int = None
    hide: bool = None
    path: str = None
    title: str = None
    icon: str = None
    component: str = None


@router.get('/v1/system/menu/list')
async def lists(
        id: str = None,
        key: int = None,
        father: int = None,
        hide: bool = None,
        path: str = None,
        title: str = None,
        icon: str = None,
        component: str = None,
        current_page: int = 1,  # 跳过
        page_size: int = 10,  # 跳过
        cfg: Config = Depends(get_config)
):
    skip = (current_page - 1) * page_size
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_MENU]

    search_menu = SearchMenu(
        key=key,
        father=father,
        hide=hide,
        path=path,
        title=title,
        icon=icon,
        component=component
    )
    query = search_menu.dict(exclude_none=True)
    if id is not None and id != '':
        query['_id'] = ObjectId(id)

    cursor = coll.find(query).skip(skip).limit(page_size)
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
async def add(menu: Menu, cfg: Config = Depends(get_config)):
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_MENU]
    doc = await coll.find_one({'key': menu.key})
    if doc:
        raise http_exp.client_err_role_key_already_exists()
    await coll.find_one_and_update(
        {'key': menu.key},
        {'$inc': {'version': 1}, '$set': menu.dict()},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    db_client.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'menu added ok'}
    )


@router.put('/v1/system/menu/edit')
async def edit(menu: Menu, cfg: Config = Depends(get_config)):
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_MENU]
    await coll.find_one_and_update(
        {'_id': ObjectId(menu.id)},
        {'$inc': {'version': 1}, '$set': menu.dict(exclude={'version', 'id'})},
    )
    db_client.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'menu edit ok'}
    )


@router.delete('/v1/system/menu/delete')
async def delete(id: str, cfg: Config = Depends(get_config)):
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_MENU]
    await coll.delete_one({'_id': ObjectId(id)})
    db_client.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'menu delete ok'}
    )
