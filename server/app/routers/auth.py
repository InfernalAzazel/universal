from datetime import timedelta

from bson import ObjectId
from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from app.cfg import Config
from app.custom_http_exception import CustomHttpException as http_exp
from app.dependencies import get_db_client_c, get_config, create_access_token, User
from app.menu_node_tree import list_to_tree
from app.models import Role
from app.settings import DATABASE_NAME, COLL_ROLE, COLL_USERS

router = APIRouter(
    prefix="/api",
    tags=["auth"],
)


@router.post('/v1/auth/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), cfg: Config = Depends(get_config)):
    """
    登录接口
    """
    if not bool(cfg.updater['init']['switch'].value):
        # 初始化配置
        raise http_exp.client_err_no_init_system_config()

    # 数据库校验
    db_client = get_db_client_c(cfg)
    doc = await db_client[DATABASE_NAME][COLL_USERS].find_one({'$and': [{'username': form_data.username}, {'password': form_data.password}]})
    if not doc:
        raise http_exp.client_err_user_or_pwd()

    temp_user = User(**doc)

    # 获取角色
    doc = await db_client[DATABASE_NAME][COLL_ROLE].find_one({'_id': ObjectId(temp_user.role_id)})

    if not doc:
        raise http_exp.server_err_get_current_user_route()

    db_client.close()
    role = Role(**doc)

    # 拼接菜单路由
    menu_nodes = list_to_tree(jsonable_encoder(role.menu_nodes), 0, is_add_redirect=True)

    # 生成访问令牌
    access_token_expires = timedelta(minutes=int(cfg.updater['jwt']['access_token_expire_minutes'].value))
    access_token = create_access_token(
        cfg,
        data={'sub': temp_user.username, 'role_name': role.name, 'menu_nodes': menu_nodes},
        expires_delta=access_token_expires
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"access_token": access_token, "token_type": "bearer"}
    )
