from configupdater import ConfigUpdater

from app.settings import ini


class Config:
    def __init__(self, file_name='settings.cfg'):
        self.file_name = file_name
        updater = ConfigUpdater()
        try:
            self.updater = updater.read('settings.cfg', 'utf-8')
        except FileNotFoundError as e:
            with open(self.file_name, 'w') as f:
                self.updater = updater.read_string(ini)
                self.updater.write(f)

    def save(self):
        """
        保存配置
        """
        with open(self.file_name, 'w') as f:
            self.updater.write(f)
