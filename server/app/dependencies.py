from datetime import datetime, timedelta
from typing import Optional, Any, TYPE_CHECKING

import motor.motor_asyncio
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from app.cfg import Config
from app.settings import DATABASE_NAME, COLL_USERS


class UserAndRole(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)
        if '_id' in data:
            self.__dict__['id'] = str(data['_id'])

    if TYPE_CHECKING:
        id: Optional[str] = None  # id
    company: Optional[str] = None  # 公司
    department: Optional[str] = None  # 部门
    username: Optional[str] = None  # 帐号： quid1111
    name: Optional[str] = None  # 姓名拼音： DeSai
    mail: Optional[str] = None  # 邮箱
    disabled: Optional[bool] = None  # 禁用：True == 禁用
    role_name: Optional[str] = None  # 角色名称： user == 普通用户
    create_time: Optional[datetime] = None  # 创建时间
    claims: Optional[dict] = None  # 认证 ````


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

app = FastAPI()


# 创建访问令牌
def create_access_token(cfg: Config, data: dict, expires_delta: Optional[timedelta] = None):
    updater = cfg.updater
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, updater['jwt']['secret_key'].value, algorithm=[int(updater['jwt']['algorithm'].value)])
    return encoded_jwt


# 或者配置文件对象
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
    updater = cfg.updater
    db_host = updater['mongodb']['db_host'].value
    db_username = updater['mongodb']['db_username'].value
    db_password = updater['mongodb']['db_password'].value
    return get_db_client(db_host, db_username, db_password)


# 获取当前用户
async def get_current_user(token: str = Depends(oauth2_scheme),
                           cfg: Config = Depends(get_config)):

    updater = cfg.updater
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, updater['jwt']['secret_key'].value, algorithms=[int(updater['jwt']['algorithm'].value)])
        username: str = payload.get("sub")
        claims: str = payload.get("claims")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db_client = get_db_client_c(cfg)
    doc = await db_client[DATABASE_NAME][COLL_USERS].find_one({'username': username})

    if doc is None:
        raise credentials_exception

    if doc is None:
        raise credentials_exception
    user_and_role = UserAndRole(**doc)
    user_and_role.claims = claims

    return user_and_role


# 获取当前活跃用户和角色
async def get_current_active_user_and_role(current_user_and_role: UserAndRole = Depends(get_current_user)):
    if current_user_and_role.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user_and_role
