import pymongo
from configupdater import ConfigUpdater
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from starlette.responses import JSONResponse

from app import settings
from app.cfg import Config
from app.dependencies import get_config
from app.env_data.role import role
from app.env_data.sub import sub
from app.env_data.users import users
from app.env_init import EnvInit
from app.custom_http_exception import CustomHttpException as http_exp

router = APIRouter(
    prefix="/api",
    tags=["init"],
)


class InitSystem(BaseModel):
    username: str
    password: str
    verify_password: str
    tz_info: str
    db_host: str
    db_username: str
    db_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str
    email_server: str
    email_domain: str
    email: str
    email_user: str
    email_pwd: str
    email_attachment_file_name: str
    push_email_task_hour: str
    push_email_task_minute: str
    push_email_task_second: str


@router.post('/v1/auth/init')
async def init(init_system: InitSystem, cfg: Config = Depends(get_config)):
    """
    初始化配置
    """
    updater = cfg.updater

    # 是否已经初始化
    if not bool(updater['init']['switch']):
        raise http_exp.client_err_re_init_system_config()

    print('[+][mongodb] db init ...')
    env_init = EnvInit(cfg)
    # 添加角色
    for v in role:
        await env_init.create_update_coll_base_data(settings.COLL_ROLE, {'name': v['name']}, v)

    # 添加超级用户
    doc = await env_init.create_update_coll_base_data(settings.COLL_USERS, {'username': users['username']}, users)
    # 添加订阅
    await env_init.create_update_coll_base_data(settings.COLL_SUB, {'userid': doc['_id']}, sub)

    # 添加数据库索引
    await env_init.create_index(
        settings.COLL_NEWS,
        [("$**", pymongo.TEXT)],
    )
    await env_init.create_index(
        settings.COLL_VULNERABILITY,
        [("$**", pymongo.TEXT)],
    )
    await env_init.create_index(
        settings.COLL_USERS,
        [("$**", pymongo.TEXT)],
    )

    updater['init']['switch'] = 'False'
    updater['shared']['tz_info'] = init_system.tz_info
    updater['mongodb']['db_host'] = init_system.db_host
    updater['mongodb']['db_username'] = init_system.db_username
    updater['mongodb']['db_password'] = init_system.db_password
    updater['email']['email_server'] = init_system.email_server
    updater['email']['email_domain'] = init_system.email_domain
    updater['email']['email'] = init_system.email
    updater['email']['email_user'] = init_system.email_user
    updater['email']['email_pwd'] = init_system.email_pwd
    updater['email']['email_attachment_file_name'] = init_system.email_attachment_file_name
    updater['push']['push_email_task_hour'] = init_system.push_email_task_hour
    updater['push']['push_email_task_minute'] = init_system.push_email_task_minute
    updater['push']['push_email_task_second'] = init_system.push_email_task_second
    cfg.save()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={}
    )
