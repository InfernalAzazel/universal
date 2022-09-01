from datetime import datetime

import pytz
from bson import ObjectId
from fastapi import APIRouter, Depends, status, Query
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.utils.dependencies import async_db_engine, auto_current_user_permission
from app.models.system.role import SearchRole, Role
from app.models.system.users import AssociationRole, User
from app.settings import DATABASE_NAME, COLL_ROLE, COLL_USERS

router = APIRouter(
    prefix="/api",
    tags=["system"],
)


@router.get('/v1/system/role/all')
async def all(
        db_engine=Depends(async_db_engine),
        _: User = Depends(auto_current_user_permission),
):
    coll = db_engine[DATABASE_NAME][COLL_ROLE]

    cursor = coll.find({})

    try:
        data = [Role(**v) async for v in cursor]
    except Exception:
        data = []
    db_engine.close()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(data)
    )


@router.get('/v1/system/role/list')
async def lists(
        uid: str = None,
        name_zh_cn: str = None,
        name_en_us: str = None,
        create_at: list[datetime] = Query(None),
        update_at: list[datetime] = Query(None),
        current_page: int = 1,  # 跳过
        page_size: int = 10,  # 跳过
        db_engine=Depends(async_db_engine),
        _: User = Depends(auto_current_user_permission),
):
    skip = (current_page - 1) * page_size

    coll = db_engine[DATABASE_NAME][COLL_ROLE]

    search_role = SearchRole(name_zh_cn=name_zh_cn, name_en_us=name_en_us)
    query = search_role.dict(exclude_none=True)

    if uid is not None and uid != '':
        query['_id'] = ObjectId(uid)
    if update_at:
        query['update_at'] = {'$gte': update_at[0].astimezone(pytz.utc), '$lte': update_at[1].astimezone(pytz.utc)}
    if create_at:
        query['create_at'] = {'$gte': create_at[0].astimezone(pytz.utc), '$lte': create_at[1].astimezone(pytz.utc)}

    cursor = coll.find(query).skip(skip).limit(page_size)
    count = await coll.count_documents(search_role.dict(exclude_none=True))
    try:
        data = [Role(**v) async for v in cursor]
    except Exception:
        data = []
    db_engine.close()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({'data': data, 'total': count})
    )


@router.post('/v1/system/role/add')
async def add(
        role: Role,
        db_engine=Depends(async_db_engine),
        _: User = Depends(auto_current_user_permission),
):
    coll = db_engine[DATABASE_NAME][COLL_ROLE]
    role.create_at = datetime.now(tz=pytz.utc)
    await coll.insert_one(role.dict(exclude_none=True))
    db_engine.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'Role added ok'}
    )


@router.put('/v1/system/role/edit')
async def edit(
        role: Role,
        db_engine=Depends(async_db_engine),
        _: User = Depends(auto_current_user_permission),
):
    coll = db_engine[DATABASE_NAME][COLL_ROLE]
    role.update_at = datetime.now(tz=pytz.utc)
    await coll.find_one_and_update(
        {'_id': ObjectId(role.uid)},
        {'$set': role.dict(exclude={'uid', 'create_at'})},
    )
    # 更新用户的角色名称
    coll = db_engine[DATABASE_NAME][COLL_USERS]
    association_role = AssociationRole(
        uid=role.uid,
        name_zh_cn=role.name_zh_cn,
        name_en_us=role.name_en_us
    )
    await coll.update_many(
        {'association_role.uid': role.uid},
        {'$set': {'association_role': association_role.dict(exclude_none=True)}},
    )
    db_engine.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'Role edit ok'}
    )


@router.delete('/v1/system/role/delete')
async def delete(
        uid: str,
        db_engine=Depends(async_db_engine),
        _: User = Depends(auto_current_user_permission),
):
    coll = db_engine[DATABASE_NAME][COLL_ROLE]
    await coll.delete_one({'_id': ObjectId(uid)})
    # 用户的角色名称加入提示 并且 禁用用户使用不存在的该角色
    # 注: 三个*用来标识被删除的角色
    coll = db_engine[DATABASE_NAME][COLL_USERS]
    association_role = AssociationRole(
        uid='***',
        name_zh_cn='***',
        name_en_us='***'
    )
    data = {
        **{'association_role': association_role.dict()},
        **{'disabled': True}
    }

    await coll.update_many(
        {'association_role.uid': uid},
        {'$set': data},
    )
    db_engine.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'Role delete ok'}
    )
