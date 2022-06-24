from datetime import datetime, timedelta
from typing import Optional

from configupdater import ConfigUpdater
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
import motor.motor_asyncio
from app.settings import DATABASE_URL, DATABASE_NAME, COLL_USERS

from app.settings import SECRET_KEY, ALGORITHM


class UserAndRole(BaseModel):
    id: Optional[str] = None  # id
    company: Optional[str] = None  # 公司
    department: Optional[str] = None  # 部门
    username: Optional[str] = None  # 帐号： quid1111
    name: Optional[str] = None  # 姓名拼音： DeSai
    mail: Optional[str] = None  # 邮箱
    disabled: Optional[bool] = None  # 禁用：True == 禁用
    role_name: Optional[str] = None  # 角色名称： user == 普通用户
    create_time: Optional[str] = None  # 创建时间
    claims: Optional[dict] = None  # 认证 ````


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

app = FastAPI()


# 创建访问令牌
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 获取当前用户
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        claims: str = payload.get("claims")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db_client = get_db_client()
    doc = await db_client[DATABASE_NAME][COLL_USERS].find_one({'username': username})

    if doc is None:
        raise credentials_exception

    user_and_role = UserAndRole()
    user_and_role.id = str(doc['_id'])
    user_and_role.company = str(doc['company'])
    user_and_role.department = str(doc['department'])
    user_and_role.username = str(doc['username'])
    user_and_role.name = str(doc['name'])
    user_and_role.mail = str(doc['mail'])
    user_and_role.disabled = doc['disabled']
    user_and_role.role_name = str(doc['role_name'])
    user_and_role.create_time = str(doc['create_time'])
    user_and_role.claims = claims

    return user_and_role


# 获取当前活跃用户和角色
async def get_current_active_user_and_role(current_user_and_role: UserAndRole = Depends(get_current_user)):
    if current_user_and_role.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user_and_role


# 获取数据库客户端
def get_db_client():
    return motor.motor_asyncio.AsyncIOMotorClient(
        DATABASE_URL
    )


def get_conf():
    updater = ConfigUpdater()
    updater.read('settings.cfg', 'utf-8')
    updater.write()
