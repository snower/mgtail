# -*- coding: utf-8 -*-
# 15/6/27
# create by: snower

import os
import configparser

class ConfFileNotFoundError(Exception):
    pass

__config = {}

DEFAULT_CONFIG = {
    "LOG_FILE": "/var/log/funsun.log",
    "LOG_LEVEL": "ERROR",
    "LOG_FORMAT": "",

    "BIND_ADDRESS": "127.0.0.1",
    "PORT": 6455,

    "SESSION_PATH": "/tmp",

    "MONGO_URL": "127.0.0.1",
    "COLLECTIONS": [],
}

def get(name, default=None):
    return __config.get(name, default)

def set(name, value):
    old_value = __config[name]
    __config[name] = value
    return old_value

def update(config):
    __config.update(config)
    return __config

update(DEFAULT_CONFIG)
for key, value in DEFAULT_CONFIG.items():
    env_value = os.environ.get(key)
    if env_value is not None:
        try:
            if isinstance(value, int):
                set(key, int(env_value))
            elif isinstance(value, float):
                set(key, float(env_value))
            elif isinstance(value, (str, bytes)):
                set(key, str(env_value))
        except:pass

def load_conf(filename):
    try:
        with open(filename, "r") as fp:
            conf_content = "[global]\n" + fp.read()
            cf = configparser.ConfigParser(allow_no_value=True)
            cf.read_string(conf_content)

            for key, value in DEFAULT_CONFIG.items():
                try:
                    if key.startswith("STORE_"):
                        conf_value = cf.get("store", key[6:].lower())
                    elif key.startswith("ACTION_"):
                        conf_value = cf.get("action", key[7:].lower())
                    elif key.startswith("EXTENSION"):
                        if key == "EXTENSIONS":
                            conf_value = cf.get("extension", "extensions")
                            if isinstance(conf_value, str):
                                set(key, conf_value.split(";"))
                                continue
                        else:
                            conf_value = cf.get("extension", key[10:].lower())
                    else:
                        conf_value = cf.get("global", key.lower())

                    try:
                        if isinstance(value, str):
                            set(key, int(conf_value))
                        elif isinstance(value, float):
                            set(key, float(conf_value))
                        elif isinstance(value, str):
                            set(key, str(conf_value))
                    except:
                        pass
                except (configparser.NoOptionError, configparser.NoSectionError):
                    continue
    except IOError:
        raise ConfFileNotFoundError()