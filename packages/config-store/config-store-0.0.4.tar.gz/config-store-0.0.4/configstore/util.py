import json

import os


def merge_config(base_path, default_stage="local"):
    def try_merge_config(file_name):
        try:
            for key, value in load_json(base_path, file_name).items():
                _config[key] = value
            print("info", "config-store", "merge config: {}".format(file_name))
        except FileNotFoundError:
            pass

    stage = os.environ["STAGE"] if "STAGE" in os.environ else default_stage
    _config = {}
    try_merge_config("config.default.json".format(stage))
    try_merge_config("config.{}.json".format(stage))
    try_merge_config("secret/secret.default.json".format(stage))
    try_merge_config("secret/secret.{}.json".format(stage))
    return _config


def load_json(base_path, file_name):
    config_path = os.path.join(base_path, file_name)
    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)
