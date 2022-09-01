from datetime import datetime

import pymongo
import pytz
from bson import ObjectId
from fastapi import APIRouter, Depends, status, Query
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.utils.dependencies import  async_db_engine, auto_current_user_permission
from app.models.system.interface import SearchInterface, Interface
from app.models.system.users import User
from app.settings import DATABASE_NAME, COLL_INTERFACE, COLL_ROLE

router = APIRouter(
    prefix="/api",
    tags=["system"],
)


@router.get('/v1/system/interface/all')
async def all(
        db_engine=Depends(async_db_engine),
        _: User = Depends(auto_current_user_permission),
):
    coll = db_engine[DATABASE_NAME][COLL_INTERFACE]

    cursor = coll.find({}).sort([
        ('group', pymongo.ASCENDING),
    ])
    try:
        data = [SearchInterface(**x) async for x in cursor]
    except Exception as _:
        data = []
    db_engine.close()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(data)
    )


@router.get('/v1/system/interface/list')
async def lists(
        uid: str = None,
        path: str = None,
        group: str = None,
        describe_zh_cn: str = None,
        describe_en_us: str = None,
        method: str = None,
        create_at: list[datetime] = Query(None),
        update_at: list[datetime] = Query(None),
        current_page: int = 1,  # 跳过
        page_size: int = 10,  # 跳过
        db_engine=Depends(async_db_engine),
        _: User = Depends(auto_current_user_permission),
):
    skip = (current_page - 1) * page_size
    coll = db_engine[DATABASE_NAME][COLL_INTERFACE]

    search_interface = SearchInterface(
        path=path,
        group=group,
        describe_zh_cn=describe_zh_cn,
        describe_en_us=describe_en_us,
        method=method,
    )

    query = search_interface.dict(exclude_none=True)

    if uid is not None and uid != '':
        query['_id'] = ObjectId(uid)
    if update_at:
        query['update_at'] = {'$gte': update_at[0].astimezone(pytz.utc), '$lte': update_at[1].astimezone(pytz.utc)}
    if create_at:
        query['create_at'] = {'$gte': create_at[0].astimezone(pytz.utc), '$lte': create_at[1].astimezone(pytz.utc)}

    cursor = coll.find(query).skip(skip).limit(page_size).sort([
        ('group', pymongo.ASCENDING),
    ])
    count = await coll.count_documents(query)
    try:
        data = [Interface(**x) async for x in cursor]
    except Exception as _:
        data = []
    db_engine.close()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({'data': data, 'total': count})
    )


@router.post('/v1/system/interface/add')
async def add(
        interface: Interface,
        db_engine=Depends(async_db_engine),
        _: User = Depends(auto_current_user_permission),
):

    coll = db_engine[DATABASE_NAME][COLL_INTERFACE]
    interface.create_at = datetime.now(pytz.utc)
    await coll.insert_one(interface.dict())
    db_engine.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'interface added ok'}
    )


@router.put('/v1/system/interface/edit')
async def edit(
        interface: Interface,
        db_engine=Depends(async_db_engine),
        _: User = Depends(auto_current_user_permission),
):
    coll = db_engine[DATABASE_NAME][COLL_INTERFACE]
    interface.update_at = datetime.now(pytz.utc)
    await coll.find_one_and_update(
        {'_id': ObjectId(interface.uid)},
        {'$set': interface.dict(exclude={'uid', 'create_at'})},
    )
    db_engine.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'interface edit ok'}
    )


@router.delete('/v1/system/interface/delete')
async def delete(
        uid: str,
        db_engine=Depends(async_db_engine),
        _: User = Depends(auto_current_user_permission)
):
    coll = db_engine[DATABASE_NAME][COLL_ROLE]
    await coll.update_many(
        {},
        {'$pull': {
            'interface_permission': {'uid': uid}
        }})
    coll = db_engine[DATABASE_NAME][COLL_INTERFACE]
    await coll.delete_one({'_id': ObjectId(uid)})
    db_engine.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'interface delete ok'}
    )
