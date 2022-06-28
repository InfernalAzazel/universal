role = [
    {
        "name": "user",
        "route": [
            {
                "path": "/vulnerability",
                "name": "vulnerability",
                "meta": {
                    "title": "message.menu.vulnerability",
                    "icon": "database-outlined",
                    "power": {
                        "see": True,
                        "operate": False
                    }
                }
            },
            {
                "path": "/power",
                "name": "power",
                "meta": {
                    "title": "message.menu.power",
                    "icon": "UserOutlined",
                    "power": {
                        "see": False,
                        "operate": False
                    }
                }
            },
            {
                "path": "/account",
                "name": "account",
                "meta": {
                    "title": "message.menu.account",
                    "icon": "UserOutlined",
                    "power": {
                        "see": True,
                        "operate": True
                    }
                }
            }
        ]
    },
    {
        "name": "admin",
        "route": [
            {
                "path": "/vulnerability",
                "name": "vulnerability",
                "meta": {
                    "title": "message.menu.vulnerability",
                    "icon": "database-outlined",
                    "power": {
                        "see": True,
                        "operate": True
                    }
                }
            },
            {
                "path": "/power",
                "name": "power",
                "meta": {
                    "title": "message.menu.power",
                    "icon": "UserOutlined",
                    "power": {
                        "see": True,
                        "operate": True
                    }
                }
            },
            {
                "path": "/account",
                "name": "account",
                "meta": {
                    "title": "message.menu.account",
                    "icon": "UserOutlined",
                    "type": 'account',
                    "power": {
                        "see": True,
                        "operate": True
                    }
                }
            }
        ]
    }
]
