from fastapi import APIRouter, Depends
from app.models.common import ResponseModel
from app.models.system.interface import InterfaceResponseModel
from app.models.system.menu import MenuResponseModel
from app.models.system.role import RoleResponseModel
from app.models.system.user import UserResponseModel
from app.utils.custom_response import ResponseMessages
from app.utils.dependencies import async_db_engine, get_language
from app.utils.env_init import EnvInit

router = APIRouter(
    prefix="/api",
    tags=["public"],
    responses={
        200: {"model": ResponseModel},
        422: {"model": ResponseModel}
    }
)


# 自动
@router.get('/v1/public/init/auto')
async def auto(
        language: str = Depends(get_language),
        db_engine=Depends(async_db_engine)
):
    """
    初始化配置
    """

    names = [
        UserResponseModel.Config.name,
        RoleResponseModel.Config.name,
        MenuResponseModel.Config.name,
        InterfaceResponseModel.Config.name
    ]

    is_init = False
    for name in names:
        coll = db_engine[name]
        count = await coll.count_documents({})
        is_init = True if count == 0 else False
    if is_init:
        ei = EnvInit()
        await ei.import_mongodb()

    return ResponseMessages(locale=language)
