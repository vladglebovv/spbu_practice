import json

SETTINGS_FILE_NAME = "setting.json"


class Settings:
    __data = None

    def __init__(self):
        raise NotImplemented

    @classmethod
    def read_params(cls):
        with open(SETTINGS_FILE_NAME) as f_in:
            cls.__data = json.load(f_in)

    @classmethod
    def get_setting(cls):
        if not cls.__data:
            cls.read_params()
        return cls.__data


def get_settings():
    return Settings.get_setting()
