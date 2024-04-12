from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from app.api.external import auth
from app.settings import APP_NAME
from app.utils.custom_response import ExceptionResponse, ResponseMessages, StatusCode
from app.utils.db import connect
from app.utils.dependencies import get_language

from app.api.admin import interface, menu, role, users

app = FastAPI(
    title=APP_NAME,
    description=f'{APP_NAME} API',
    version="stable 0.0.1",
)


@app.on_event('startup')
async def startup():
    await connect()


@app.on_event("shutdown")
def on_shutdown():
    pass


@app.exception_handler(ExceptionResponse)
async def http_exception_handler(request: Request, exc: ExceptionResponse):
    """HTTP 异常处理程序 """
    return ResponseMessages(locale=exc.locale, status_code=exc.status_code, success=False, detail=exc.detail)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """422 客户端输入数据验证异常"""
    language: str = get_language(request)
    return ResponseMessages(locale=language, status_code=StatusCode.bad_request, success=False, detail=str(exc))


# app.include_router(init.router)
# app.include_router(auth.router)
# app.include_router(info.router)
# # 系统
# app.include_router(monitor.router)
# app.include_router(users.router)
# app.include_router(menu.router)
# app.include_router(role.router)
# app.include_router(interface.router)

# app.mount('/', StaticFiles(directory='app/static/docs/developer', html=True), name='static')

app.include_router(auth.router)


app.include_router(interface.router)
app.include_router(menu.router)
app.include_router(role.router)
app.include_router(users.router)
