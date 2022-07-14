from datetime import datetime, timedelta
from typing import Optional

import motor.motor_asyncio
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.cfg import Config
from app.models import User
from app.settings import DATABASE_NAME, COLL_USERS

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


# 创建访问令牌
def create_access_token(cfg: Config, data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    key = cfg.updater['jwt']['secret_key'].value
    algorithm = cfg.updater['jwt']['algorithm'].value
    encoded_jwt = jwt.encode(to_encode, key, algorithm)

    return encoded_jwt


# 获取配置文件对象
async def get_config():
    return Config()


# 获取数据库客户端
def get_db_client(db_host, db_username, db_password):
    return motor.motor_asyncio.AsyncIOMotorClient(
        f'mongodb://{db_username}:{db_password}@{db_host}'
    )


# 获取数据库客户端C
def get_db_client_c(cfg: Config):
    """
    配置文件对象
    """
    db_host = cfg.updater['mongodb']['db_host'].value
    db_username = cfg.updater['mongodb']['db_username'].value
    db_password = cfg.updater['mongodb']['db_password'].value
    return get_db_client(db_host, db_username, db_password)


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
        key = cfg.updater['jwt']['secret_key'].value
        algorithm = cfg.updater['jwt']['algorithm'].value
        payload = jwt.decode(token, key, [algorithm])
        username: str = payload.get("sub")
        menu_nodes: str = payload.get("menu_nodes")
        role_name: str = payload.get("role_name")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db_client = get_db_client_c(cfg)
    doc = await db_client[DATABASE_NAME][COLL_USERS].find_one({'username': username})

    db_client.close()

    if doc is None:
        raise credentials_exception
    # **{**doc, 'role_name': role_name, 'menu_nodes': menu_nodes}
    user = User(**{**doc, 'role_name': role_name, 'menu_nodes': menu_nodes})
    print(user)
    return user


# 获取当前活跃用户
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
