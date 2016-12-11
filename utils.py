import configparser
import random
import string
from timeit import default_timer

CONFIG_FILE = "database.ini"
CONFIG = configparser.ConfigParser()
CONFIG.read(CONFIG_FILE)


def get_database_config_from_file():
    config_to_use = CONFIG.get("global", "use_db_config")

    engine = CONFIG[config_to_use]['engine']
    host = CONFIG[config_to_use]['host']
    user = CONFIG[config_to_use]['user']
    password = CONFIG[config_to_use]['password']
    db = CONFIG[config_to_use]['db']

    return "%s://%s:%s@%s/%s" % (engine, user, password, host, db)


def get_batch_size():
    return CONFIG['runner'].getint('batch_size')


class SimpleTimer:
    def __init__(self, start_time=0.0):
        self.start_time = start_time

    def start(self):
        self.start_time = default_timer()

    def get_time(self):
        return default_timer() - self.start_time

    @staticmethod
    def create_and_start():
        return SimpleTimer(default_timer())


def generate_random_id(n=5):
    return ''.join(''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n)))
