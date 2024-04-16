from zoneinfo import ZoneInfo

import motor.motor_asyncio
from beanie import init_beanie

from app.models.admin import Interface, User, Menu, Role
from app.settings import MONGODB_USERNAME, MONGODB_PASSWORD, MONGODB_HOST, TZ_INFO, MONGODB_DATABASE_NAME


def async_db_engine():
    return motor.motor_asyncio.AsyncIOMotorClient(
        f'mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}',
        tz_aware=True,
        tzinfo=ZoneInfo(TZ_INFO)
    )[MONGODB_DATABASE_NAME]


async def connect():
    client = async_db_engine()
    models = [
        User,
        Interface,
        Menu,
        Role
    ]
    return await init_beanie(database=client, document_models=models)
