import json
import os

from bson import json_util

from app.settings import DATABASE_NAME, COLL_USERS, COLL_ROLE, COLL_INTERFACE, COLL_MENU
from app.utils.dependencies import sync_db_engine


class EnvInit:
    mongodb_path = 'app' + os.sep + 'database' + os.sep + 'mongodb'

    def __init__(self, storage_method=0):
        """
        保存方式

        storage_method=0 系统备份
        storage_method=1 全部备份
        """
        self.storage_method = storage_method

    def import_mongodb(self):
        """
        导入 JSON 到 MongoDB
        """

        client = sync_db_engine()
        for name in os.listdir(self.mongodb_path):
            coll_name = name.split('.')[0]
            with open(self.mongodb_path + os.sep + name, 'r', encoding='utf-8') as f:
                data = json_util.loads(f.read())
                # 这里需要检查一下 data 是否为空 list，否则会报错
                if data:
                    client[DATABASE_NAME][coll_name].insert_many(data)
        client.close()

    def export_mongodb(self):
        """
        导出 MongoDB 到 JSON
        """
        client = sync_db_engine()
        names = []
        match self.storage_method:
            case 0:
                names = [COLL_USERS, COLL_ROLE, COLL_MENU, COLL_INTERFACE]
            case 1:
                names = client[DATABASE_NAME].list_collection_names()
        for name in names:
            doc = client[DATABASE_NAME][name].find({})
            data = [v for v in doc]
            with open(f'{self.mongodb_path}{os.sep}{name}.json', 'w', encoding='utf-8') as f:
                json.dump(json.loads(json_util.dumps(data)), f, ensure_ascii=False, indent=2, separators=(',', ':'))
        client.close()
