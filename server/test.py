from configupdater import ConfigUpdater

# cfg = """
# [metadata]
# author = Ada Lovelace
# summary = The Analytical Engine
# """
#
# updater = ConfigUpdater()
# updater.read_string(cfg)
# updater["metadata"]["license"] = "MIT"
#
# print(updater.to_dict())


updater = ConfigUpdater()
try:
    updater.read('settings.cfg', 'utf-8')
except FileNotFoundError as e:
    updater.write()