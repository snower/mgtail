# -*- coding: utf-8 -*-
# 15/6/27
# create by: snower

import os
from .utils import string_type, number_type

__config = {}

DEFAULT_CONFIG = {
    "LOG_FILE": "/var/log/funsun.log",
    "LOG_LEVEL": "ERROR",
    "LOG_FORMAT": "",

    "BIND_ADDRESS": "0.0.0.0",
    "PORT": 6455,
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
            if isinstance(value, number_type):
                set(key, int(env_value))
            elif isinstance(value, float):
                set(key, float(env_value))
            elif isinstance(value, string_type):
                set(key, str(env_value))
        except:pass