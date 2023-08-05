# Introduction

config_bat is a package helps developers easily config the app using config.json file.

# Getting Started

1. Installation process:

```
pip install config_bat
```

2. Usage:

Getting config: if there is no config in config.json, return default_value

```
from config_bat import config
your_config = config.get("config_key",default_value)
```

The default_value is optional, if default_value is not provided, the function will return None.

3. API references:

**Environment variables:**

The package behavior can be overrided by export these environment variables:

CONFIG_PATH: the path to config file. Default: "/config/config.json".

APP_STAGE: define in config.json.

**config.json file:**

The first level key is the stage of the app. You can define the config nested in those keys.

The "common" key is readed by default. If the config apears both in "common" and other stages, the stage config will be used.

If you want to use environmen variables, place a "\$" character before you variable name.

Example of config.json:

```
{
  "common": {
    // Environmental variables
    "JWT_SECRET": "$SEC_KEY",
    "port": 8080
  },
  "development": {
   // Nested config
    "mongodb": {
      "host": "localhost",
      "user": "dev_user",
      "pass": "dev_pass"
    }
  },
  "production": {
    "mongodb": {
      "host": "your.domain",
      "user": "prod_user",
      "pass": "prod_pass"
    }
  }
}
```
