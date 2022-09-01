from datetime import datetime, timedelta
from typing import Optional
from zoneinfo import ZoneInfo

import casbin
import motor.motor_asyncio
from bson import ObjectId
from fastapi import Depends, HTTPException, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.models.system.role import Role
from app.models.system.syslog import SysLog
from app.models.system.users import User
from app.settings import DATABASE_NAME, COLL_USERS, COLL_ROLE, COLL_SYSLOG, MONGODB_USERNAME, MONGODB_PASSWORD, \
    MONGODB_HOST, TZ_INFO, JWT_ALGORITHM, JWT_SECRET
from app.utils.custom_adapter import Adapter
from pymongo import MongoClient

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


# 创建访问令牌
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, JWT_ALGORITHM)

    return encoded_jwt


# 获取数据库客户端 异步引擎
def async_db_engine():
    return motor.motor_asyncio.AsyncIOMotorClient(
        f'mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}',
        tz_aware=True,
        tzinfo=ZoneInfo(TZ_INFO)
    )


# 获取数据库客户端 同步引擎
def sync_db_engine():
    return MongoClient(
        f'mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}',
        tz_aware=True,
        tzinfo=ZoneInfo(TZ_INFO)
    )


# 获取当前用户
async def get_current_user(
        token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, [JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db_client = async_db_engine()
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

    db_client = async_db_engine()
    # 只对 创建 修改 删除做记录
    if method != 'GET':
        # 插入系统日志
        coll = db_client[DATABASE_NAME][COLL_SYSLOG]
        await coll.insert_one(syslog)

    coll = db_client[DATABASE_NAME][COLL_ROLE]
    doc = await coll.find_one({'_id': ObjectId(current_user.association_role.uid)})

    # 获取角色失败
    if not doc:
        raise HTTPException(status_code=400, detail="Failed to get role")
    role = Role(**doc)

    db_client.close()
    # 设置适配器
    adapter = Adapter(doc)
    e = casbin.Enforcer('rbac_model.conf', adapter)
    # # 验证接口权限
    if e.enforce(role.uid, path, method):
        pass
    else:
        raise HTTPException(status_code=403, detail="Permission denied")
    return current_user
