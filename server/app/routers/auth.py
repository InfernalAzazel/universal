from datetime import timedelta

from configupdater import ConfigUpdater
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from app.cfg import Config
from app.custom_http_exception import CustomHttpException as http_exp
from app.dependencies import create_access_token, get_db_client_c, get_config
from app.settings import DATABASE_NAME, COLL_USERS, COLL_ROLE

router = APIRouter(
    prefix="/api",
    tags=["auth"],
)


@router.post('/v1/auth/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), cfg: Config = Depends(get_config)):
    """
    登录接口
    """
    updater = cfg.updater
    if bool(updater['init']['switch'].value):
        # 初始化配置
        raise http_exp.client_err_no_init_system_config()

    # 数据库校验
    db_client = get_db_client_c(updater)
    doc = await db_client[DATABASE_NAME][COLL_USERS].find_one(
        {'username': form_data.username},
        {'password': form_data.password},
    )
    if not doc:
        raise http_exp.client_err_user_or_pwd()

    # 获取角色
    role = await db_client[DATABASE_NAME][COLL_ROLE].find_one({'name': doc['role_name']})

    if not role:
        raise http_exp.server_err_get_current_user_route()

    db_client.close()

    # 生成访问令牌
    access_token_expires = timedelta(minutes=int(updater['jwt']['access_token_expire_minutes'].value))
    access_token = create_access_token(
        updater,
        data={"sub": doc['username'], 'claims': role},
        expires_delta=access_token_expires
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"access_token": access_token, "token_type": "bearer"}
    )
