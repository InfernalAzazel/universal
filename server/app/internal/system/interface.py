from typing import Any, TYPE_CHECKING

from bson import ObjectId
from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.responses import JSONResponse

from app.cfg import Config
from app.dependencies import get_config, get_db_client_c
from app.settings import DATABASE_NAME, COLL_INTERFACE

router = APIRouter(
    prefix="/api",
    tags=["system"],
)


class Interface(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)
        for k, v in list(data.items()):
            if k == '_id':
                self.__dict__['id'] = str(data[k])
                data.pop(k)
            else:
                self.__dict__[k] = v

    def __setattr__(self, key, value):
        if key == 'id':
            self.__dict__['id'] = str(value)
        super().__setattr__(key, value)

    if TYPE_CHECKING:
        id: str = None
    path: str
    group: str
    describe: str
    method: str


class GroupInterface(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)
        for k, v in list(data.items()):
            if k == '_id':
                self.__dict__['id'] = str(data[k])
                self.__dict__['describe'] = str(data[k])
                data.pop(k)
    id: str = None
    describe: str = None
    children: list[Interface] = None


class SearchInterface(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)
        for k, v in list(data.items()):
            if v == '':
                self.__dict__[k] = None
            else:
                self.__dict__[k] = v

    if TYPE_CHECKING:
        id: str = None
    path: str = None
    group: str = None
    describe: str = None
    method: str = None


@router.get('/v1/system/interface/group')
async def group(
        cfg: Config = Depends(get_config)
):
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_INTERFACE]

    pipeline = [
        {'$group': {'_id': '$group', 'children': {'$push': '$$ROOT'}}},
    ]
    cursor = coll.aggregate(pipeline)
    try:
        data = [GroupInterface(**x) async for x in cursor]
    except Exception as _:
        data = []
        print(_)
    db_client.close()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(data)
    )


@router.get('/v1/system/interface/list')
async def lists(
        id: str = None,
        path: str = None,
        group: str = None,
        describe: str = None,
        method: str = None,
        current_page: int = 1,  # 跳过
        page_size: int = 10,  # 跳过
        cfg: Config = Depends(get_config)
):
    skip = (current_page - 1) * page_size
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_INTERFACE]

    search_interface = SearchInterface(
        path=path,
        group=group,
        describe=describe,
        method=method,
    )

    query = search_interface.dict(exclude_none=True)
    if id is not None and id != '':
        query['_id'] = ObjectId(id)

    cursor = coll.find(query).skip(skip).limit(page_size)
    count = await coll.count_documents(query)
    try:
        data = [Interface(**x) async for x in cursor]
    except Exception as _:
        data = []
    db_client.close()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({'data': data, 'total': count})
    )


@router.post('/v1/system/interface/add')
async def add(interface: Interface, cfg: Config = Depends(get_config)):
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_INTERFACE]
    await coll.insert_one(interface.dict())
    db_client.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'interface added ok'}
    )


@router.put('/v1/system/interface/edit')
async def edit(interface: Interface, cfg: Config = Depends(get_config)):
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_INTERFACE]
    await coll.find_one_and_update(
        {'_id': ObjectId(interface.id)},
        {'$inc': {'version': 1}, '$set': interface.dict(exclude={'version', 'id'})},
    )
    db_client.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'interface edit ok'}
    )


@router.delete('/v1/system/interface/delete')
async def delete(id: str, cfg: Config = Depends(get_config)):
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_INTERFACE]
    await coll.delete_one({'_id': ObjectId(id)})
    db_client.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'interface delete ok'}
    )
