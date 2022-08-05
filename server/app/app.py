from fastapi import FastAPI

from app.internal.system import menu, role, interface, users, syslog, settings
from app.routers import auth, init

app = FastAPI(
    title="Universal",
    description="Universal API",
    version="stable 0.0.1",
)


# 路由
app.include_router(auth.router)
app.include_router(init.router)
app.include_router(users.router)
app.include_router(menu.router)
app.include_router(role.router)
app.include_router(interface.router)
app.include_router(syslog.router)
app.include_router(settings.router)


# app.mount('/', StaticFiles(directory='app/static/dist', html=True), name='static')


@app.on_event('startup')
async def startup():
    pass
