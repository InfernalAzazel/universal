from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.models.system.settings import Settings
from app.utils.cfg import Config
from app.utils.custom_http_exception import CustomHttpException as http_exp
from app.utils.dependencies import get_config
from app.utils.env_init import EnvInit

router = APIRouter(
    prefix="/api",
    tags=["init"],
)


@router.get('/v1/auth/init/state')
async def state(cfg: Config = Depends(get_config)):
    """
    初始化配置
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'switch': cfg.updater['init']['switch']},
    )


@router.get('/v1/auth/init/data')
async def data(cfg: Config = Depends(get_config)):
    if not bool(cfg.updater['init']['switch']):
        raise http_exp.client_err_re_init_system_config()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(cfg.updater),
    )


@router.put('/v1/auth/init/system')
async def system(settings: Settings, cfg: Config = Depends(get_config)):
    """
    初始化配置
    """
    # 是否已经初始化
    if not bool(cfg.updater['init']['switch']):
        raise http_exp.client_err_re_init_system_config()

    settings.init.switch = False
    cfg.updater.update(settings.dict(exclude_none=True))
    cfg.save()

    # 数据库初始化
    ei = EnvInit()
    ei.import_mongodb()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={}
    )
