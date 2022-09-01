from fastapi import APIRouter, status, Depends
from starlette.responses import JSONResponse

from app.settings import COLL_USERS, COLL_ROLE, COLL_MENU, COLL_INTERFACE, DATABASE_NAME
from app.utils.dependencies import async_db_engine
from app.utils.env_init import EnvInit

router = APIRouter(
    prefix="/api",
    tags=["init"],
)


@router.get('/v1/auth/init')
async def state(db_engine=Depends(async_db_engine)):
    """
    初始化配置
    """
    names = [COLL_USERS, COLL_ROLE, COLL_MENU, COLL_INTERFACE]

    init = False
    for name in names:
        coll = db_engine[DATABASE_NAME][name]
        count = await coll.count_documents({})
        if count == 0:
            init = True
        else:
            init = False
    if init:
        ei = EnvInit()
        ei.import_mongodb()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'code': 200},
    )
