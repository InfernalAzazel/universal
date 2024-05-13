from zoneinfo import ZoneInfo

import motor.motor_asyncio
from bunnet import init_bunnet
from pymongo import MongoClient

from app.models.admin import Interface, User, Menu, Role
from app.settings import MONGODB_USERNAME, MONGODB_PASSWORD, MONGODB_HOST, TZ_INFO, MONGODB_DATABASE_NAME


def async_db_engine():
    return motor.motor_asyncio.AsyncIOMotorClient(
        f'mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}',
        tz_aware=True,
        tzinfo=ZoneInfo(TZ_INFO)
    )[MONGODB_DATABASE_NAME]


def connect():
    client = MongoClient(
        f'mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}',
        tz_aware=True,
        tzinfo=ZoneInfo(TZ_INFO)
    )[MONGODB_DATABASE_NAME]
    models = [
        User,
        Interface,
        Menu,
        Role,
        # 业务
    ]
    # 使用 Product 文档类和数据库初始化 bunnet
    return init_bunnet(database=client, document_models=models)
