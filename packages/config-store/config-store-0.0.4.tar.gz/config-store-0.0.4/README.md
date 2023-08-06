# config-store
A python module for env variable and config file management. 
Inspired from webpack configuration management, config-store support multi-stage configs merger.
For information security, separation of sensitive settings are also provided.

## Installation
```bash
pip install configstore
```

## Usage
```python
import configstore
configstore.connect($CONFIG_FOLDER)
print(configstore.get("foo", default_value="not found QQ"))
# >>> 'bar'
```

## Config Setting
```
CONFIG_FOLDER
- secret
    - secret.default.json
    - secret.dev.json 
    - secret.pd.json
- config.default.json [requried]
- config.dev.json 
- config.pd.json 
```
Config Read Order
1. ENV variable
2. stage config
3. default config
4. default value

