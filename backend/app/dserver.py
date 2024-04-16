from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.settings import APP_NAME

app = FastAPI(
    title=APP_NAME,
    description=f'{APP_NAME} API',
    version="stable 0.0.1",
)

app.mount('/', StaticFiles(directory='app/static/docs/developer', html=True), name='static')


@app.on_event('startup')
async def startup():
    pass
