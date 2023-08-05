from cpbox.tool.utils import Singleton
import os

class ConfigData():
    __metaclass__ = Singleton

    def __init__(self):
        self._env = os.environ['PUPPY_ENV'] if 'PUPPY_ENV' in os.environ else 'dev'
        self._app_name = None
        self._data = {}

    def get_env(self):
        return self._env

    def get_app_name(self):
        return self._app_name

    def init(self, app_name, env = None, config = {}):
        self._app_name = app_name
        if env is not None:
            self._env = env
        self._data = config

    def get_config(self):
        return self._data

    def get(self, key, fallback = None):
        return self._data.get(key, fallback)

appconfig = ConfigData()
