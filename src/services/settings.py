import os
import json


class Settings:
    def __init__(self, config_path='config/config.json'):
        with open(config_path) as f:
            self.__config = json.load(f)

    def __get_setting_key(self, key):
        if not key in self.__config:
            raise KeyError(f"Setting '{key}' must be in config file")
        return os.environ.get(key, self.__config[key])

    def get(self, key):
        setting = self.__get_setting_key(key)
        if not setting:
            raise KeyError(f"Setting '{key}' is empty")
        return setting
