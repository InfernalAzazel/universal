from typing import Annotated
from zoneinfo import ZoneInfo
import motor.motor_asyncio
import pymongo
from pydantic import WrapValidator
from app.settings import MONGODB_USERNAME, MONGODB_PASSWORD, MONGODB_HOST, TZ_INFO, MONGODB_DATABASE_NAME

PyObjectId = Annotated[str, WrapValidator(lambda v, h: str(v))]


def async_db_engine():
    return motor.motor_asyncio.AsyncIOMotorClient(
        f'mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}',
        tz_aware=True,
        tzinfo=ZoneInfo(TZ_INFO)
    )[MONGODB_DATABASE_NAME]


async def pagination_query(coll, query, ppq):
    skip = (ppq.current_page - 1) * ppq.page_size
    cursor = coll.find(query).skip(skip).limit(ppq.page_size).sort([
        ('group', pymongo.ASCENDING),
    ])
    total = await coll.count_documents(query)
    data = [x async for x in cursor]
    return data, total
