
from dynaconf import Dynaconf


class AppConfig:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance=super().__new__(cls)
        return cls._instance
    def __init__(self):
        if not hasattr(self , '_initialized'):
            self.settings = Dynaconf(
                envvar_prefix="MSC_GENIE",
                settings_files=['settings.yaml', '.secrets.yaml'],
            )
            self._initialized=True
    def get(self, key:str):
        return self.settings[key]

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
