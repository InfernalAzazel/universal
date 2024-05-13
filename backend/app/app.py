from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from app.api.admin.dashboard import monitor
from app.api.admin.system import interface, menu, role, users
from app.api.external import auth
from app.api.root import info
from app.settings import APP_NAME
from app.utils.api_response import ExceptionResponse, APIResponse, StatusCode
from app.utils.db import connect

app = FastAPI(
    title=APP_NAME,
    description=f'{APP_NAME} API',
    version="stable 0.0.1",
)


@app.on_event('startup')
def startup():
    connect()


@app.on_event("shutdown")
def on_shutdown():
    pass


@app.exception_handler(ExceptionResponse)
def http_exception_handler(request: Request, exc: ExceptionResponse):
    """HTTP 异常处理程序 """
    return APIResponse(success=False, code=exc.code, detail=exc.detail)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    """422 客户端输入数据验证异常"""
    return APIResponse(success=False, code=StatusCode.bad_request.value, detail=str(exc))


# 公开
app.include_router(auth.router)

# 系统
app.include_router(interface.router)
app.include_router(menu.router)
app.include_router(role.router)
app.include_router(users.router)
app.include_router(monitor.router)

# 业务
app.include_router(info.router)

# app.mount('/', StaticFiles(directory='app/static/docs/developer', html=True), name='static')
