from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models.admin import User
from app.models.common import ResponseModel, ResponseLoginModel
from app.settings import JWT_MINUTES
from app.utils.api_response import APIResponse, StatusCode
from app.utils.jwt import create_access_token

router = APIRouter(
    prefix="/api/v1",
    tags=["external"],
    responses={
        200: {"model": ResponseLoginModel},
        422: {"model": ResponseModel}
    }
)


@router.post('/auth/login')
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    登录接口
    """

    # 数据库校验
    user: Optional[User] = ~User.find_one(User.username == form_data.username)

    if not user:
        return APIResponse(success=False, code=StatusCode.credentials_invalid.value)

    # 生成访问令牌
    access_token_expires = timedelta(minutes=JWT_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username},
        expires_delta=access_token_expires
    )
    return APIResponse(access_token=access_token, token_type="bearer")
