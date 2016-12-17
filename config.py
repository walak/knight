from configparser import ConfigParser
from getopt import getopt
from os import getenv

import sys


class AppConfiguration:
    def __init__(self, file):
        self.config = ConfigParser()
        self.file = file
        self.used_configuration = None

    def init(self):
        self.config.read(self.file)

    def get_db_config(self):
        return self.config.get("global", "use_db_config")

    def get_db_url(self):
        config_to_use = self.get_db_config()

        engine = self.config[config_to_use]['engine']
        host = self.config[config_to_use]['host']
        user = self.config[config_to_use]['user']
        password = self.config[config_to_use]['password']
        db = self.config[config_to_use]['db']

        return "%s://%s:%s@%s/%s" % (engine, user, password, host, db)

    def get_batch_size(self):
        return self.config['runner'].getint('batch_size')

    @staticmethod
    def empty():
        return AppConfiguration(None)

    @staticmethod
    def from_file(file):
        cfg = AppConfiguration(file)
        cfg.init()
        return cfg


class AppConfigProvider:
    ENV_NAME = "KNIGHT_CONFIG"

    def get_config_file_from_env_variable(self):
        return getenv(AppConfigProvider.ENV_NAME)

    def get_env(self):
        return getenv(AppConfigProvider.ENV_NAME, default="prod")

    def get_config_file_from_command_line(self):
        opts, _ = getopt(sys.argv[1:], "c", ["config="])
        for o, a in opts:
            if o == "--config" and a is not None:
                return a
        return None

    def get_config_from_file(self, file):
        if not file is None:
            return AppConfiguration.from_file(file)
        else:
            raise RuntimeError("No config file defined")

    def get_config(self):
        if self.is_test():
            return AppConfiguration.empty()
        file = self.get_config_file_from_command_line()
        if file is None:
            file = self.get_config_file_from_env_variable()
        return self.get_config_from_file(file)

    def is_test(self):
        return self.get_env() == "test"
