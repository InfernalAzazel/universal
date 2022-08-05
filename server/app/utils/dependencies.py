from datetime import datetime, timedelta
from typing import Optional

import casbin
import motor.motor_asyncio
import pytz
from bson import ObjectId
from fastapi import Depends, HTTPException, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.utils.cfg import Config
from app.models.system.users import User
from app.models.system.syslog import SysLog
from app.models.system.role import Role
from app.settings import DATABASE_NAME, COLL_USERS, COLL_ROLE, COLL_SYSLOG
from app.utils.custom_adapter import Adapter

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


# 创建访问令牌
def create_access_token(cfg: Config, data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    key = cfg.updater['jwt']['secret_key']
    algorithm = cfg.updater['jwt']['algorithm']
    encoded_jwt = jwt.encode(to_encode, key, algorithm)

    return encoded_jwt


# 获取配置文件对象
async def get_config() -> Config:
    return Config()


# 获取数据库客户端
def get_db_client(db_host, db_username, db_password, tz_info):
    return motor.motor_asyncio.AsyncIOMotorClient(
        f'mongodb://{db_username}:{db_password}@{db_host}',
        tz_aware=True,
        tzinfo=pytz.timezone(tz_info)
    )


# 获取数据库客户端C
def get_db_client_c(cfg: Config):
    """
    配置文件对象
    """
    db_host = cfg.updater['mongodb']['host']
    db_username = cfg.updater['mongodb']['username']
    db_password = cfg.updater['mongodb']['password']
    tz_info = cfg.updater['shared']['tz_info']
    return get_db_client(db_host, db_username, db_password, tz_info)


# 获取当前用户
async def get_current_user(
        token: str = Depends(oauth2_scheme),
):
    cfg = await get_config()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        key = cfg.updater['jwt']['secret_key']
        algorithm = cfg.updater['jwt']['algorithm']
        payload = jwt.decode(token, key, [algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db_client = get_db_client_c(cfg)
    doc = await db_client[DATABASE_NAME][COLL_USERS].find_one({'username': username})
    db_client.close()

    if doc is None:
        raise credentials_exception

    user = User(**doc)

    return user


# 自动用户认证权限
async def auto_current_user_permission(request: Request, current_user: User = Depends(get_current_user)):
    path = request.url.path
    method = request.method
    host = request.client.host
    os = str(request.headers.get('sec-ch-ua-platform'))
    browser = request.headers.get('user-agent')
    query_params = str(dict(request.query_params.items()))
    body = (await request.body()).decode('utf-8')

    syslog = jsonable_encoder(SysLog(
        username=current_user.username,
        host=host,
        browser=browser,
        os=os,
        path=path,
        query_params=query_params,
        method=method,
        text=body
    ))

    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    cfg = await get_config()
    db_client = get_db_client_c(cfg)
    # 只对 创建 修改 删除做记录
    if method != 'GET':
        # 插入系统日志
        coll = db_client[DATABASE_NAME][COLL_SYSLOG]
        await coll.insert_one(syslog)

    coll = db_client[DATABASE_NAME][COLL_ROLE]
    doc = await coll.find_one({'_id': ObjectId(current_user.association_role.id)})

    # 获取角色失败
    if not doc:
        raise HTTPException(status_code=400, detail="Failed to get role")
    role = Role(**doc)

    db_client.close()
    # 设置适配器
    adapter = Adapter(doc)
    e = casbin.Enforcer('rbac_model.conf', adapter)
    # # 验证接口权限
    if e.enforce(role.id, path, method):
        pass
    else:
        raise HTTPException(status_code=403, detail="Permission denied")
    return current_user
