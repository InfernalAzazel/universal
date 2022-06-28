from configupdater import ConfigUpdater
from pymongo import ReturnDocument

from app import settings
from app.cfg import Config
from app.dependencies import get_db_client_c


class EnvInit:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.updater = cfg.updater

    async def create_index(self, coll_name, key):
        """
        创建索引
        """
        str_search = 'str_search'
        db_client = get_db_client_c(self.cfg)
        coll = db_client[settings.DATABASE_NAME][coll_name]
        index = await coll.index_information()
        print(index)
        if str_search in index.keys():
            coll.drop_index(str_search)
            coll.create_index(key, name=str_search)
        else:
            coll.create_index(key, name=str_search)
        index = await coll.index_information()
        print(index)
        print(
            f'[+][create_index] mongodb  coll_name:{coll_name} name: {str_search} data: ' + ''.join(
                str([index[str_search]])))
        db_client.close()

    async def create_update_coll_base_data(self, coll_name, query: dict, set_data):
        """
        创建或者更新集合基本数据
        查询数据
        """
        db_client = get_db_client_c(self.cfg)
        coll = db_client[settings.DATABASE_NAME][coll_name]
        doc = await coll.find_one_and_update(
            query,
            {'$set': set_data},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        print(f'[+][create_update_coll_base_data] mongodb coll_name:{coll_name} update or insert ok...')
        db_client.close()
        return doc
