import os
import json

configPath = os.getenv("CONFIG_PATH", "config/config.json")

if configPath[:1] == "/":
    # If the first letter is "/", consider the path as absolute path
    filePath = configPath
else:
    # Else consider the path relative path
    filePath = os.path.join(os.getcwd(), configPath)

appStage = os.getenv("APP_STAGE", "development")


class Config:
    def __init__(self):
        try:
            with open(filePath, "r") as fileObj:
                self.config = json.loads(fileObj.read())
        except FileNotFoundError:
            print("Warning: no config file found")
            self.config = {}

    def get(self, keys, default=None):

        try:
            return self.getData(appStage, keys, default)
        except KeyError:
            try:
                return self.getData("common", keys, default)
            except KeyError:
                return default

    def getData(self, section, keys, default):
        keyList = keys.split(".")
        data = self.config[section]
        for key in keyList:
            data = data[key]
        if isinstance(data, str):
            if data[:1] == "$":
                return os.getenv(data[1:], default)
        return data


config = Config()

print(config.get("mongodb.database"))
