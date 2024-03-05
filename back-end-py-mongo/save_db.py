import asyncio
from app.utils.env_init import EnvInit

ei = EnvInit()
asyncio.run(ei.export_mongodb())
