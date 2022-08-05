import os

import rtoml
from pathlib import Path


class Config:
    default_file_name = 'settings.default.toml'

    def __init__(self, file_name='settings.toml'):
        self.path = Path(os.getcwd() + os.sep + file_name)
        try:
            self.updater = rtoml.load(self.path)
        except FileNotFoundError:
            self.updater = rtoml.load(Path(os.getcwd() + os.sep + self.default_file_name))
            self.updater['init']['switch'] = True
            self.save()

    def save(self):
        """
        保存配置
        """
        rtoml.dump(self.updater, self.path, pretty=True)
