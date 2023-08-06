import configstore
import os
config_path = os.path.join(os.path.dirname(__file__), 'configs')


if __name__ == '__main__':
    configstore.connect(config_path)
    print(configstore.get('debug'))
    print(configstore.get('key'))
    configstore.connect(config_path, stage='dev')
    print(configstore.get('debug'))
