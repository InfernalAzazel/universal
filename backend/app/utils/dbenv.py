import json
import os
from bson import json_util
from app.models.admin import User, Role, Menu, Interface
from app.utils.db import async_db_engine


class DBenv:
    database_path = os.path.join(os.getcwd(), 'app', 'database')

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
        for name in os.listdir(self.database_path):
            coll_name = name.split('.')[0]
            with open(self.database_path + os.sep + name, 'r', encoding='utf-8') as f:
                data = json_util.loads(f.read())
                # 这里需要检查一下 data 是否为空 list，否则会报错
                if data:
                    await client[coll_name].insert_many(data)

    async def export_mongodb(self):
        """
        导出 MongoDB 到 JSON
        """
        client = async_db_engine()
        settings_names = [
            User.Settings.name,
            Role.Settings.name,
            Menu.Settings.name,
            Interface.Settings.name
        ]

        if self.storage_method == 1:
            settings_names = await client.list_collection_names()

        for name in settings_names:
            cursor = client[name].find({})
            data = [v async for v in cursor]
            with open(f'{self.database_path}{os.sep}{name}.json', 'w', encoding='utf-8') as f:
                json.dump(json.loads(json_util.dumps(data)), f, ensure_ascii=False, indent=2, separators=(',', ':'))
