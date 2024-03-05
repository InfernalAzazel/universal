from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models.common import ResponseModel, ResponseLoginModel
from app.models.system.user import UserResponseModel
from app.settings import JWT_MINUTES
from app.utils.custom_response import ExceptionResponse, StatusCode, ResponseMessages
from app.utils.db import async_db_engine
from app.utils.dependencies import get_language
from app.utils.jwt import create_access_token

router = APIRouter(
    prefix="/api",
    tags=["public"],
    responses={
        200: {"model": ResponseLoginModel},
        422: {"model": ResponseModel}
    }
)


@router.post('/v1/public/auth/login')
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        language: str = Depends(get_language),
        db_engine=Depends(async_db_engine)
):
    """
    登录接口
    """

    # 数据库校验
    doc = await db_engine[UserResponseModel.Config.name].find_one(
        {'$and': [{'username': form_data.username}, {'password': form_data.password}]})

    if not doc:
        raise ExceptionResponse(locale=language, status_code=StatusCode.username_password_error)

    user_model = UserResponseModel(**doc)

    # 生成访问令牌
    access_token_expires = timedelta(minutes=JWT_MINUTES)
    access_token = create_access_token(
        data={'sub': user_model.username},
        expires_delta=access_token_expires
    )

    return ResponseMessages(locale=language, access_token=access_token, token_type="bearer")
