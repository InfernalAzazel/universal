from configupdater import ConfigUpdater

cfg = """
# 初始化激活
[init]
switch=True
# 共用
[shared]
tz_info=1
# 数据库
[mongodb]
db_host=
db_username=
db_password=
# 令牌配置
[jwt]
secret_key=
algorithm=
access_token_expire_minutes=
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

# updater = ConfigUpdater()
# updater.read_string(cfg)
# updater["metadata"]["license"] = "MIT"
#
# print(updater.to_dict())

import os.path

print(os.path.isfile('settings.cfg'))
updater = ConfigUpdater()
try:
    updater.read('settings.cfg', 'utf-8')
except FileNotFoundError as e:
    with open('settings.cfg', 'w') as f:
        updater.read_string(cfg)
        updater["shared"]["tz_info"] = "MIT"
        print(updater["shared"]["tz_info"].value)
        print(type(updater["shared"]["tz_info"].value))
        updater.write(f)
