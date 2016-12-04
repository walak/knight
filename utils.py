import configparser

CONFIG_FILE = "database.ini"


def get_database_config_from_file():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    config_to_use = config.get("global", "use_db_config")

    engine = config[config_to_use]['engine']
    host = config[config_to_use]['host']
    user = config[config_to_use]['user']
    password = config[config_to_use]['password']
    db = config[config_to_use]['db']

    return "%s://%s:%s@%s/%s" % (engine, user, password, host, db)

