from fastapi import FastAPI

from app.internal.system import menu, role, interface, users
from app.routers import auth
from app.routers import init

app = FastAPI(
    title="Vulnerability Management System",
    description="Excellent Vulnerability Management System Solution.",
    version="stable 0.1.1",
)


# 路由
app.include_router(auth.router)
app.include_router(init.router)
app.include_router(users.router)
app.include_router(menu.router)
app.include_router(role.router)
app.include_router(interface.router)


# app.mount('/', StaticFiles(directory='app/static/dist', html=True), name='static')


@app.on_event('startup')
async def startup():
    pass
