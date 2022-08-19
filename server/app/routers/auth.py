from datetime import timedelta

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from app.utils.cfg import Config
from app.utils.custom_http_exception import CustomHttpException as http_exp
from app.utils.dependencies import get_db_client_c, get_config, create_access_token, User
from app.settings import DATABASE_NAME, COLL_USERS

router = APIRouter(
    prefix="/api",
    tags=["auth"],
)


@router.post('/v1/auth/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), cfg: Config = Depends(get_config)):
    """
    登录接口
    """
    if bool(cfg.updater['init']['switch']):
        # 初始化配置
        raise http_exp.client_err_no_init_system_config()

    # 数据库校验
    db_client = get_db_client_c(cfg)
    doc = await db_client[DATABASE_NAME][COLL_USERS].find_one({'$and': [{'username': form_data.username}, {'password': form_data.password}]})

    print(doc)
    if not doc:
        raise http_exp.client_err_user_or_pwd()

    temp_user = User(**doc)

    # 生成访问令牌
    access_token_expires = timedelta(minutes=int(cfg.updater['jwt']['minutes']))
    access_token = create_access_token(
        cfg,
        data={'sub': temp_user.username},
        expires_delta=access_token_expires
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"access_token": access_token, "token_type": "bearer"}
    )
