from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pymongo import ReturnDocument
from starlette.responses import JSONResponse

from app.dependencies import create_access_token, get_db_client, UserAndRole, get_current_active_user_and_role

from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES, DATABASE_NAME, COLL_USERS, COLL_ROLE, COLL_SUB

router = APIRouter(
    prefix="/api",
    tags=["auth"],
)


@router.post('/v1/auth/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    登录接口
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 数据库校验
    db_client = get_db_client()
    doc = await db_client[DATABASE_NAME][COLL_USERS].find_one(
        {'username': form_data.username},
        {'password': form_data.password},
    )
    if not doc:
        raise credentials_exception

    # 获取角色
    role = await db_client[DATABASE_NAME][COLL_ROLE].find_one({'name': doc['role_name']})

    if not role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to get route",
            headers={"WWW-Authenticate": "Bearer"},
        )

    db_client.close()

    # 生成访问令牌
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": doc['username'], 'claims': role}, expires_delta=access_token_expires
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"access_token": access_token, "token_type": "bearer"}
    )


@router.post('/v1/auth/refresh')
def refresh(current_user_and_role: UserAndRole = Depends(get_current_active_user_and_role)):
    """
    刷新令牌
    """
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={"sub": current_user_and_role.username, 'claims': current_user_and_role.claims},
        expires_delta=access_token_expires
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"access_token": new_access_token}
    )
