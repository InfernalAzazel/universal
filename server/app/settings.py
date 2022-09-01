import os

TZ_INFO = os.getenv('TZ_INFO', 'Asia/Shanghai')

MONGODB_HOST = os.getenv('MONGODB_HOST', '127.0.0.1')
MONGODB_USERNAME = os.getenv('MONGODB_USERNAME', 'spb0122003')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', 'dcaGRzkJpuKsHgMs8hoS')

JWT_SECRET = os.getenv('JWT_SECRET', '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
JWT_MINUTES = int(os.getenv('JWT_MINUTES', '30'))

# 数据库名称
DATABASE_NAME = 'universal'
# 集合 用户
COLL_USERS = 'users'
# 集合 角色
COLL_ROLE = 'role'
# 集合 菜单
COLL_MENU = 'menu'
# 集合 接口
COLL_INTERFACE = 'interface'
# 集合 系统日志
COLL_SYSLOG = 'syslog'
