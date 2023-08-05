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
            return self.config[appStage][key]
        except KeyError:
            try:
                return self.config["common"][key]
            except KeyError:
                return default


config = Config()
