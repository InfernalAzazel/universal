from urllib.parse import quote_plus

# Mongodb 配置 -----------------------------------------------------------------
DATABASE_URL = "mongodb://%s:%s@%s" \
               % (quote_plus('spb0122003'),
                  quote_plus('dcaGRzkJpuKsHgMs8hoS'),
                  '127.0.0.1')
# 数据库名称
DATABASE_NAME = 'universal'
# 集合 用户
COLL_USERS = 'users'
# 集合 角色
COLL_ROLE = 'role'
# 集合 新闻
COLL_NEWS = 'news'
# 集合 订阅
COLL_SUB = 'sub'
# 集合 漏洞
COLL_VULNERABILITY = 'vulnerability'

# 令牌配置 -------------------------------------------------------------------------

# jwt 加密
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# jwt 加密类型
ALGORITHM = "HS256"
# 令牌有效时间/分钟
ACCESS_TOKEN_EXPIRE_MINUTES = 30



