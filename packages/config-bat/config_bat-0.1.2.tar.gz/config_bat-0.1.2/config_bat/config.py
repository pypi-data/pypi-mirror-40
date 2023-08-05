import os
import json

configPath = os.getenv("CONFIG_PATH", os.getcwd() + "/config/config.json")


class Config:
    def __init__(self):        
        try:
            with open(configPath, "r") as fileObj:
                self.config = json.loads(fileObj.read())
        except FileNotFoundError:
            print("Warning: no config file found")
            self.config = {}

    def get(self, key, default):
        try:
            return self.config[key]
        except KeyError:
            return default

config = Config()
