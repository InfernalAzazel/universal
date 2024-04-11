from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.staticfiles import StaticFiles

from app.api.private.root import info
from app.settings import APP_NAME
from app.utils.custom_response import ExceptionResponse, ResponseMessages, StatusCode
from app.utils.dependencies import get_language

app = FastAPI(
    title=APP_NAME,
    description=f'{APP_NAME} API',
    version="stable 0.0.1",
)


@app.exception_handler(ExceptionResponse)
async def http_exception_handler(request: Request, exc: ExceptionResponse):
    """HTTP 异常处理程序 """
    return ResponseMessages(locale=exc.locale, status_code=exc.status_code, success=False, detail=exc.detail)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """422 客户端输入数据验证异常"""
    language: str = get_language(request)
    return ResponseMessages(locale=language, status_code=StatusCode.bad_request, success=False, detail=str(exc))


app.include_router(info.router)


app.mount('/', StaticFiles(directory='app/static/docs/developer', html=True), name='static')


@app.on_event('startup')
async def startup():
    pass
