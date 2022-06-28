import datetime
import pytz

tz = pytz.timezone('Asia/Shanghai')

users = {
    'company': None,
    'department': None,
    "username": "uidp8656",
    'name': None,
    'mail': None,
    "disabled": False,
    "role_name": "admin",
    "create_time": datetime.datetime.now().astimezone(tz)
}
