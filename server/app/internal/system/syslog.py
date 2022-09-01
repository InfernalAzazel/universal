from datetime import datetime

import pytz
from bson import ObjectId
from fastapi import APIRouter, Depends, status, Query
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.utils.dependencies import async_db_engine, auto_current_user_permission
from app.models.system.syslog import SysLog
from app.models.system.users import User
from app.settings import DATABASE_NAME, COLL_SYSLOG

router = APIRouter(
    prefix="/api",
    tags=["system"],
)


@router.get('/v1/system/syslog/all')
async def all(
        db_engine=Depends(async_db_engine),
        _: User = Depends(auto_current_user_permission)
):
    
    coll = db_engine[DATABASE_NAME][COLL_SYSLOG]

    cursor = coll.find({})

    try:
        data = [SysLog(**v) async for v in cursor]
    except Exception:
        data = []
    db_engine.close()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(data)
    )


@router.get('/v1/system/syslog/list')
async def lists(
        id: str = None,
        username: str = None,
        create_at: list[datetime] = Query(None),
        update_at: list[datetime] = Query(None),
        current_page: int = 1,  # 跳过
        page_size: int = 10,  # 跳过
        db_engine=Depends(async_db_engine),
        _: User = Depends(auto_current_user_permission)
):
    skip = (current_page - 1) * page_size
    
    coll = db_engine[DATABASE_NAME][COLL_SYSLOG]

    search_syslog = SysLog(username=username)
    query = search_syslog.dict(exclude_none=True)

    if id is not None and id != '':
        query['_id'] = ObjectId(id)
    if update_at:
        query['update_at'] = {'$gte': update_at[0].astimezone(pytz.utc), '$lte': update_at[1].astimezone(pytz.utc)}
    if create_at:
        query['create_at'] = {'$gte': create_at[0].astimezone(pytz.utc), '$lte': create_at[1].astimezone(pytz.utc)}

    cursor = coll.find(query).skip(skip).limit(page_size)
    count = await coll.count_documents(search_syslog.dict(exclude_none=True))
    try:
        data = [SysLog(**v) async for v in cursor]
    except Exception:
        data = []
    db_engine.close()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({'data': data, 'total': count})
    )


@router.post('/v1/system/syslog/add')
async def add(
        syslog: SysLog,
        db_engine=Depends(async_db_engine),
        _: User = Depends(auto_current_user_permission)
):
    
    coll = db_engine[DATABASE_NAME][COLL_SYSLOG]
    syslog.create_at = datetime.now(tz=pytz.utc)
    await coll.insert_one(syslog.dict(exclude_none=True))
    db_engine.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'Role added ok'}
    )


@router.put('/v1/system/syslog/edit')
async def edit(
        syslog: SysLog,
        db_engine=Depends(async_db_engine),
        _: User = Depends(auto_current_user_permission)
):
    
    coll = db_engine[DATABASE_NAME][COLL_SYSLOG]
    syslog.update_at = datetime.now(tz=pytz.utc)
    await coll.find_one_and_update(
        {'_id': ObjectId(syslog.id)},
        {'$set': syslog.dict(exclude={'id', 'create_at'})},
    )

    db_engine.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'Role edit ok'}
    )


@router.delete('/v1/system/syslog/delete')
async def delete(
        uid: str,
        db_engine=Depends(async_db_engine),
        _: User = Depends(auto_current_user_permission)
):
    
    coll = db_engine[DATABASE_NAME][COLL_SYSLOG]
    await coll.delete_one({'_id': ObjectId(uid)})
    db_engine.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'Role delete ok'}
    )
