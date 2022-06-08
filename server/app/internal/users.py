import datetime as dt
from datetime import datetime
from typing import Optional

import jieba
import pytz
from bson import ObjectId
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from pymongo import ReturnDocument
from starlette.responses import JSONResponse

from app.dependencies import UserAndRole, get_current_active_user_and_role, get_db_client
from app.settings import DATABASE_NAME, COLL_USERS, COLL_SUB

router = APIRouter(
    prefix="/api",
    tags=["users"],
)


class User(BaseModel):
    company: Optional[str] = None  # 公司
    department: Optional[str] = None  # 部门
    username: Optional[str] = None  # 帐号： quid1111
    name: Optional[str] = None  # 姓名拼音： DeSai
    mail: Optional[str] = None  # 邮箱
    disabled: Optional[bool] = False  # 禁用：True == 禁用
    role_name: Optional[str] = None  # 角色名称： user == 普通用户


@router.get('/v1/users/account')
async def account(current_user_and_role: UserAndRole = Depends(get_current_active_user_and_role)):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=current_user_and_role.dict()
    )


@router.put('/v1/users/update')
async def update(
        id: str,
        user: User,
        current_user_and_role: UserAndRole = Depends(get_current_active_user_and_role)
):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'action': 'OK'}
    )
