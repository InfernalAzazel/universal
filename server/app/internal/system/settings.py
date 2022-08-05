from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.models.system.settings import Settings
from app.models.system.users import User
from app.utils.cfg import Config
from app.utils.dependencies import get_config, auto_current_user_permission

router = APIRouter(
    prefix="/api",
    tags=["system"],
)


@router.get('/v1/system/settings/data')
async def data(
        cfg: Config = Depends(get_config),
        _: User = Depends(auto_current_user_permission)
):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(cfg.updater)
    )


@router.get('/v1/system/settings/default')
async def default(
        _: User = Depends(auto_current_user_permission)
):
    cfg = Config(Config.default_file_name)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(cfg.updater)
    )


@router.put('/v1/system/settings/edit')
async def edit(
        settings: Settings,
        cfg: Config = Depends(get_config),
        _: User = Depends(auto_current_user_permission),
):
    cfg.updater.update(settings.dict())
    cfg.save()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'settings edit ok'}
    )
