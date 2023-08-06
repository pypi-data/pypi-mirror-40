import os

from configstore.util import merge_config

name = "config-store"

config = {}


def connect(base_path, stage='local'):
    global config
    config = merge_config(base_path, stage)
    return config


def get(key, default_value=None):
    # 1. env
    if key in os.environ:
        values = os.environ[key].split()
        return values if len(values) > 1 else values[0]
    # 2. config.json
    try:
        if key in config:
            return config[key]
        else:
            raise KeyError("{} not found in config".format(key))
    # 3. default value
    except Exception as e:
        if default_value is not None:
            return default_value
        else:
            raise e
