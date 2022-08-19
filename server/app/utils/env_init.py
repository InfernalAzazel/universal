import json
import os
from bson import json_util
from pymongo import MongoClient
from app.models.system.settings import Settings
from app.settings import DATABASE_NAME
from app.utils.cfg import Config


class EnvInit:
    mongodb_path = 'app' + os.sep + 'database' + os.sep + 'mongodb'

    def __init__(self):
        self.cfg = Config()
        self.settings = Settings(**self.cfg.updater)

    def __mongo_client(self):
        return MongoClient(
            f'mongodb://{self.settings.mongodb.username}:{self.settings.mongodb.password}@{self.settings.mongodb.host}'
        )

    def import_mongodb(self):
        """
        导入 JSON 到 MongoDB
        """
        client = self.__mongo_client()
        for name in os.listdir(self.mongodb_path):
            coll_name = name.split('.')[0]
            with open(self.mongodb_path + os.sep + name, 'r', encoding='utf-8') as f:
                data = json_util.loads(f.read())
                # 过滤空值，空值会引发插入异常
                if data:
                    client[DATABASE_NAME][coll_name].insert_many(data)
        client.close()

    def export_mongodb(self):
        """
        导出 MongoDB 到 JSON
        """
        client = self.__mongo_client()
        names = client[DATABASE_NAME].list_collection_names()
        for name in names:
            doc = client[DATABASE_NAME][name].find({})
            data = [v for v in doc]
            with open(f'{self.mongodb_path}{os.sep}{name}.json', 'w', encoding='utf-8') as f:
                json.dump(json.loads(json_util.dumps(data)), f, ensure_ascii=False, indent=2, separators=(',', ':'))
        client.close()
