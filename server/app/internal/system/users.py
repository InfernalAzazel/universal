from datetime import datetime

from bson import ObjectId
from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from pymongo import ReturnDocument
from starlette.responses import JSONResponse

from app.dependencies import get_current_active_user, get_config, get_db_client_c, get_current_user
from app.custom_http_exception import CustomHttpException as http_exp
from app.cfg import Config
from app.models import User
from app.settings import DATABASE_NAME, COLL_USERS

router = APIRouter(
    prefix="/api",
    tags=["users"],
)


@router.get('/v1/users/account')
async def account(
        current_user: User = Depends(get_current_active_user),
        cfg: Config = Depends(get_config)
):
    content = jsonable_encoder(current_user)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content
    )


@router.get('/v1/users/list')
async def lists(
        id: str = None,
        role_id: str = None,
        role_name: str = None,
        username: str = None,
        name: str = None,
        mail: str = None,
        company: str = None,
        department: str = None,
        disabled: bool = None,
        create_time: datetime = None,
        current_page: int = 1,  # 跳过
        page_size: int = 10,  # 跳过
        cfg: Config = Depends(get_config)
):
    skip = (current_page - 1) * page_size
    db_client = get_db_client_c(cfg)

    coll = db_client[DATABASE_NAME][COLL_USERS]

    search_User = User(
        id=id,
        role_id=role_id,
        role_name=role_name,
        username=username,
        name=name,
        mail=mail,
        company=company,
        department=department,
        disabled=disabled,
        create_time=create_time,
    )

    query = search_User.dict(exclude_none=True)
    if id is not None and id != '':
        query['_id'] = ObjectId(id)

    cursor = coll.find(query).skip(skip).limit(page_size)
    count = await coll.count_documents(query)
    try:
        data = [User(**x) async for x in cursor]
    except Exception as _:
        print(_)
        data = []
    db_client.close()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({'data': data, 'total': count})
    )


@router.post('/v1/users/add')
async def add(user: User, cfg: Config = Depends(get_config)):
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_USERS]
    doc = await coll.find_one({'username': user.username})
    if doc:
        raise http_exp.client_err_role_key_already_exists()

    await coll.find_one_and_update(
        {'username': user.username},
        {'$inc': {'version': 1}, '$set': user.dict()},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    db_client.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'user added ok'}
    )


@router.put('/v1/users/edit')
async def edit(user: User, cfg: Config = Depends(get_config)):
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_USERS]
    await coll.find_one_and_update(
        {'_id': ObjectId(user.id)},
        {'$inc': {'version': 1}, '$set': user.dict(exclude={'version', 'id'})},
    )
    db_client.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'user edit ok'}
    )


@router.delete('/v1/users/delete')
async def delete(id: str, cfg: Config = Depends(get_config)):
    db_client = get_db_client_c(cfg)
    coll = db_client[DATABASE_NAME][COLL_USERS]
    await coll.delete_one({'_id': ObjectId(id)})
    db_client.close()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'menu delete ok'}
    )
