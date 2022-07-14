import json

import uvicorn
from bson import ObjectId
from pymongo import MongoClient

db_host = '127.0.0.1'
db_username = 'spb0122003'
db_password = 'dcaGRzkJpuKsHgMs8hoS'


# 获取数据库客户端
def get_db_client():
    return MongoClient(
        f'mongodb://{db_username}:{db_password}@{db_host}'
    )


db_client = get_db_client()
coll = db_client['universal']['menu']
# root_children
menus = [
    {
        'key': 1,
        'father': 0,
        'hide': True,
        'path': '/login',
        'component': 'layout/login.vue',
        'title': '登录',
        'icon': 'House',

    }, {
        'key': 2,
        'father': 0,
        'hide': True,
        'path': '/init',
        'component': 'layout/init.vue',
        'title': '初始化',
        'icon': 'House',

    },
    {
        'key': 3,
        'father': 0,
        'hide': False,
        'path': '/',
        'component': 'layout/base.vue',
        'title': '首页',
        'icon': 'House',

    },
    {
        'key': 4,
        'father': 3,
        'hide': False,
        'path': '/home',
        'component': 'views/home/index.vue',
        'title': '首页',
        'icon': 'Home',
    },
    {
        'key': 5,
        'father': 0,
        'hide': False,
        'path': '/system',
        'title': 'system',
        'icon': 'Setting',
        'component': 'layout/base.vue',
    },
    {
        'key': 6,
        'father': 5,
        'hide': False,
        'path': '/system/menu',
        'title': 'menu',
        'icon': 'CreditCard',
        'component': 'views/system/menu/index.vue',
    },
    {
        'key': 7,
        'father': 5,
        'hide': False,
        'path': '/system/role',
        'title': 'role',
        'icon': 'Bicycle',
        'component': 'views/system/role/index.vue',

    },
    {
        'key': 8,
        'father': 5,
        'hide': False,
        'path': '/system/role111',
        'title': 'role111',
        'icon': 'Bicycle',
        'component': 'views/system/role/index.vue',

    },
    {
        'key': 9,
        'father': 5,
        'hide': False,
        'path': '/system/role456',
        'title': 'role456',
        'icon': 'Bicycle',
        'component': 'views/system/role/index.vue',

    },
    {
        'key': 10,
        'father': 9,
        'hide': False,
        'path': '/system/role222',
        'title': 'role222',
        'icon': 'Bicycle',
        'component': 'views/system/role/index.vue',

    },
]


# print(json.dumps({'data': menus}))
# coll.insert_many(menus)
# doc = coll.find({'_id': ObjectId('62c79bef76a04c01fd6d6568')})
# print([i for i in doc])
