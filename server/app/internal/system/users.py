from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter, Depends, status, Query
from fastapi.encoders import jsonable_encoder
from pymongo import ReturnDocument
from datetime import timezone
from starlette.responses import JSONResponse
from app.utils.custom_http_exception import CustomHttpException as http_exp
from app.utils.dependencies import auto_current_user_permission, async_db_engine
from app.utils.menu_node_tree import list_to_tree
from app.models.system.users import User
from app.models.system.role import Role
from app.settings import DATABASE_NAME, COLL_USERS, COLL_ROLE

router = APIRouter(
    prefix="/api",
    tags=["users"],
)


@router.get('/v1/users/account')
async def account(
        current_user: User = Depends(auto_current_user_permission),
):
    content = jsonable_encoder(current_user)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content
    )


@router.get('/v1/users/routes')
async def routers(
        current_user: User = Depends(auto_current_user_permission),
        db_engine=Depends(async_db_engine)
):
    doc = await db_engine[DATABASE_NAME][COLL_ROLE].find_one({'_id': ObjectId(current_user.association_role.uid)})
    if not doc:
        raise http_exp.server_err_get_current_user_route()

    role = Role(**doc)

    # 拼接菜单路由
    menu_permission = list_to_tree(jsonable_encoder(role.menu_permission), 0, is_add_redirect=True)
    content = jsonable_encoder(menu_permission)

    db_engine.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content
    )


@router.get('/v1/users/list')
async def lists(
        uid: str = None,
        username: str = None,
        name: str = None,
        mail: str = None,
        company: str = None,
        department: str = None,
        disabled: bool = None,
        association_role_uid: str = None,
        create_at: list[datetime] = Query(None),
        update_at: list[datetime] = Query(None),
        current_page: int = 1,  # 跳过
        page_size: int = 10,  # 跳过
        db_engine=Depends(async_db_engine),
        _: User = Depends(auto_current_user_permission)

):
    skip = (current_page - 1) * page_size

    coll = db_engine[DATABASE_NAME][COLL_USERS]

    search_user = User(
        uid=uid,
        username=username,
        name=name,
        mail=mail,
        company=company,
        department=department,
        disabled=disabled,
    )

    query = search_user.dict(exclude_none=True)
    if uid is not None and uid != '':
        query['_id'] = ObjectId(uid)
    if update_at:
        query['update_at'] = {'$gte': update_at[0].astimezone(timezone.utc),
                              '$lte': update_at[1].astimezone(timezone.utc)}
    if create_at:
        query['create_at'] = {'$gte': create_at[0].astimezone(timezone.utc),
                              '$lte': create_at[1].astimezone(timezone.utc)}
    if association_role_uid is not None and association_role_uid != '':
        query['association_role.uid'] = association_role_uid

    cursor = coll.find(query).skip(skip).limit(page_size)
    count = await coll.count_documents(query)
    try:
        data = [User(**x) async for x in cursor]
    except Exception as _:
        data = []
    db_engine.close()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({'data': data, 'total': count})
    )


@router.post('/v1/users/add')
async def add(
        user: User,
        db_engine=Depends(async_db_engine),
        _: User = Depends(auto_current_user_permission)
):
    coll = db_engine[DATABASE_NAME][COLL_USERS]
    doc = await coll.find_one({'username': user.username})
    if doc:
        raise http_exp.client_err_role_key_already_exists()
    user.create_at = datetime.now(tz=timezone.utc)
    await coll.find_one_and_update(
        {'username': user.username},
        {'$set': user.dict()},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    db_engine.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'user added ok'}
    )


@router.put('/v1/users/edit')
async def edit(
        user: User,
        db_engine=Depends(async_db_engine),
        _: User = Depends(auto_current_user_permission),
):
    coll = db_engine[DATABASE_NAME][COLL_USERS]
    user.update_at = datetime.now(tz=timezone.utc)
    await coll.find_one_and_update(
        {'_id': ObjectId(user.uid)},
        {'$set': user.dict(exclude={'uid', 'create_at'})},
    )
    db_engine.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'user edit ok'}
    )


@router.delete('/v1/users/delete')
async def delete(
        uid: str,
        db_engine=Depends(async_db_engine),
        _: User = Depends(auto_current_user_permission),
):
    coll = db_engine[DATABASE_NAME][COLL_USERS]
    await coll.delete_one({'_id': ObjectId(uid)})
    db_engine.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'menu delete ok'}
    )
