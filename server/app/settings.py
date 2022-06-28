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


ini = """
# 初始化激活-程序变量请问请勿设置
[init]
switch=True
# 共用
[shared]
tz_info=Asia/Shanghai
# 数据库
[mongodb]
db_host=127.0.0.1
db_username=spb0122003
db_password=dcaGRzkJpuKsHgMs8hoS
# 令牌配置
[jwt]
secret_key=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
algorithm=HS256
access_token_expire_minutes=30
# 邮箱
[email]
email_server=
email_domain=
email=
email_user=
email_pwd=
email_attachment_file_name=
# 定时推送任务
[push]
push_email_task_hour=
push_email_task_minute=
push_email_task_second=
"""
