import os
import json

configPath = os.getenv("CONFIG_PATH", os.getcwd() + "/config/config.json")
appStage = os.getenv("APP_STAGE", "development")


class Config:
    def __init__(self):
        try:
            with open(configPath, "r") as fileObj:
                self.config = json.loads(fileObj.read())
        except FileNotFoundError:
            print("Warning: no config file found")
            self.config = {}

    def get(self, key, default=None):

        try:
            return self.getData(appStage, key, default)
        except KeyError:
            try:
                return self.getData("common", key, default)
            except KeyError:
                return default

    def getData(self, section, key, default):
        data = self.config[section][key]
        if data[:1] == "$":
            return os.getenv(data[1:], default)
        return data


config = Config()
