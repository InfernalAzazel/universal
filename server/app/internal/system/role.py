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
from app.settings import DATABASE_NAME, COLL_ROLE

router = APIRouter(
    prefix="/api",
    tags=["system"],
)


class Role(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)
        for k, v in data.items():
            if k == '_id':
                self.__dict__['id'] = str(data['_id'])
            else:
                self.__dict__[k] = data[k]

    if TYPE_CHECKING:
        id: str = None
    key: str
    name: str
    description: str
    menu_nodes: list[dict] = []
    interface_nodes: list[dict] = []


class SearchRole(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)
        for k, v in data.items():
            if k == 'key' and v == '':
                self.__dict__['key'] = None
            elif k == 'name' and v == '':
                self.__dict__['name'] = None
            else:
                self.__dict__[k] = data[k]

    key: str = None
    name: str = None


@router.get('/v1/system/role/list')
async def lists(
        key: str = None,
        name: str = None,
        current_page: int = 1,  # 跳过
        page_size: int = 10,  # 跳过
        cfg: Config = Depends(get_config)
):
    skip = (current_page - 1) * page_size
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_ROLE]

    search_role = SearchRole(key=key, name=name)
    query = search_role.dict(exclude_none=True)

    cursor = coll.find(query).skip(skip).limit(page_size)
    count = await coll.count_documents(search_role.dict(exclude_none=True))
    try:
        data = [Role(**v) async for v in cursor]
    except Exception:
        data = []
    db_client.close()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({'data': data, 'total': count})
    )


@router.get('/v1/system/role/one')
async def one(id: str, cfg: Config = Depends(get_config)):
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_ROLE]
    doc = await coll.find_one({'_id': ObjectId(id)})
    if not doc:
        raise http_exp.client_err_role_not_found()
    db_client.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(Role(**doc))
    )


@router.post('/v1/system/role/add')
async def add(role: Role, cfg: Config = Depends(get_config)):
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_ROLE]
    doc = await coll.find_one({'key': role.key})
    if doc:
        raise http_exp.client_err_role_key_already_exists()
    await coll.find_one_and_update(
        {'key': role.key},
        {'$inc': {'version': 1}, '$set': role.dict()},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    db_client.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'Role added ok'}
    )


@router.put('/v1/system/role/edit')
async def edit(role: Role, cfg: Config = Depends(get_config)):
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_ROLE]
    await coll.find_one_and_update(
        {'_id': ObjectId(role.id)},
        {'$inc': {'version': 1}, '$set': role.dict(exclude={'version', 'id'})},
    )
    db_client.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'Role edit ok'}
    )


@router.delete('/v1/system/role/delete')
async def delete(id: str, cfg: Config = Depends(get_config)):
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_ROLE]
    await coll.delete_one({'_id': ObjectId(id)})
    db_client.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'Role delete ok'}
    )
