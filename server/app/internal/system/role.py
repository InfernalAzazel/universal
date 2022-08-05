from datetime import datetime

import pytz
from bson import ObjectId
from fastapi import APIRouter, Depends, status, Query
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.utils.cfg import Config
from app.utils.dependencies import get_config, get_db_client_c, auto_current_user_permission
from app.models.system.role import SearchRole, Role
from app.models.system.users import AssociationRole, User
from app.settings import DATABASE_NAME, COLL_ROLE, COLL_USERS

router = APIRouter(
    prefix="/api",
    tags=["system"],
)


@router.get('/v1/system/role/all')
async def all(
        cfg: Config = Depends(get_config),
        current_user: User = Depends(auto_current_user_permission),
):
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_ROLE]

    cursor = coll.find({})

    try:
        data = [Role(**v) async for v in cursor]
    except Exception:
        data = []
    db_client.close()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(data)
    )


@router.get('/v1/system/role/list')
async def lists(
        id: str = None,
        name_zh_cn: str = None,
        name_en_us: str = None,
        create_at: list[datetime] = Query(None),
        update_at: list[datetime] = Query(None),
        current_page: int = 1,  # 跳过
        page_size: int = 10,  # 跳过
        cfg: Config = Depends(get_config),
        current_user: User = Depends(auto_current_user_permission),
):
    skip = (current_page - 1) * page_size
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_ROLE]

    search_role = SearchRole(name_zh_cn=name_zh_cn, name_en_us=name_en_us)
    query = search_role.dict(exclude_none=True)

    if id is not None and id != '':
        query['_id'] = ObjectId(id)
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
    db_client.close()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({'data': data, 'total': count})
    )


@router.post('/v1/system/role/add')
async def add(
        role: Role,
        cfg: Config = Depends(get_config),
   current_user: User = Depends(auto_current_user_permission),
):
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_ROLE]
    role.create_at = datetime.now(tz=pytz.utc)
    await coll.insert_one(role.dict(exclude_none=True))
    db_client.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'Role added ok'}
    )


@router.put('/v1/system/role/edit')
async def edit(
        role: Role,
        cfg: Config = Depends(get_config),
        current_user: User = Depends(auto_current_user_permission),
):
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_ROLE]
    role.update_at = datetime.now(tz=pytz.utc)
    await coll.find_one_and_update(
        {'_id': ObjectId(role.id)},
        {'$set': role.dict(exclude={'id', 'create_at'})},
    )
    # 更新用户的角色名称
    coll = db_client[DATABASE_NAME][COLL_USERS]
    association_role = AssociationRole(
        id=role.id,
        name_zh_cn=role.name_zh_cn,
        name_en_us=role.name_en_us
    )
    await coll.update_many(
        {'association_role.id': role.id},
        {'$set': {'association_role': association_role.dict(exclude_none=True)}},
    )
    db_client.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'Role edit ok'}
    )


@router.delete('/v1/system/role/delete')
async def delete(
        id: str,
        cfg: Config = Depends(get_config),
   current_user: User = Depends(auto_current_user_permission),
):
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_ROLE]
    await coll.delete_one({'_id': ObjectId(id)})
    # 用户的角色名称加入提示 并且 禁用用户使用不存在的该角色
    # 注: 三个*用来标识被删除的角色
    coll = db_client[DATABASE_NAME][COLL_USERS]
    association_role = AssociationRole(
        id='***',
        name_zh_cn='***',
        name_en_us='***'
    )
    data = {
        **{'association_role': association_role.dict()},
        **{'disabled': True}
    }

    await coll.update_many(
        {'association_role.id': id},
        {'$set': data},
    )
    db_client.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'Role delete ok'}
    )
