import json
import os
from bson import json_util
from app.utils.db import async_db_engine
from app.models.system.interface import InterfaceResponseModel
from app.models.system.menu import MenuResponseModel
from app.models.system.role import RoleResponseModel
from app.models.system.user import UserResponseModel


class EnvInit:
    mongodb_path = 'app' + os.sep + 'database'

    def __init__(self, storage_method=0):
        """
        保存方式

        storage_method=0 系统备份
        storage_method=1 全部备份
        """
        self.storage_method = storage_method

    async def import_mongodb(self):
        """
        导入 JSON 到 MongoDB
        """

        client = async_db_engine()
        for name in os.listdir(self.mongodb_path):
            coll_name = name.split('.')[0]
            with open(self.mongodb_path + os.sep + name, 'r', encoding='utf-8') as f:
                data = json_util.loads(f.read())
                # 这里需要检查一下 data 是否为空 list，否则会报错
                if data:
                    await client[coll_name].insert_many(data)

    async def export_mongodb(self):
        """
        导出 MongoDB 到 JSON
        """
        client = async_db_engine()
        names = []
        match self.storage_method:
            case 0:
                names = [
                    InterfaceResponseModel.Config.name,
                    RoleResponseModel.Config.name,
                    MenuResponseModel.Config.name,
                    UserResponseModel.Config.name
                ]
            case 1:
                names = await client.list_collection_names()
        for name in names:
            cursor = client[name].find({})
            data = [v async for v in cursor]
            with open(f'{self.mongodb_path}{os.sep}{name}.json', 'w', encoding='utf-8') as f:
                json.dump(json.loads(json_util.dumps(data)), f, ensure_ascii=False, indent=2, separators=(',', ':'))
