import asyncio
from zoneinfo import ZoneInfo

from beanie import init_beanie, Document
from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient

from app.settings import MONGODB_USERNAME, MONGODB_PASSWORD, MONGODB_HOST, TZ_INFO, MONGODB_DATABASE_NAME


class Interface(Document):
    title: str = None
    path: str = None
    group: str = None
    method: str = None

    class Settings:
        name = "interface"


async def example():
    client = AsyncIOMotorClient(
        f'mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}',
        tz_aware=True,
        tzinfo=ZoneInfo(TZ_INFO)
    )[MONGODB_DATABASE_NAME]

    await init_beanie(database=client, document_models=[Interface])

    data = await Interface.find({'_id': ObjectId('62cd16f41db5004e1234d3d8')}).to_list()

    print(jsonable_encoder(data, by_alias=False))
    data = await Interface.get('62cd16f41db5004e1234d3d8')
    print(data.dict())


if __name__ == "__main__":
    asyncio.run(example())
