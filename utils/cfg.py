import configparser


def config(cfg='config.ini'):
    config = configparser.ConfigParser()
    config.read(cfg)
    return config
