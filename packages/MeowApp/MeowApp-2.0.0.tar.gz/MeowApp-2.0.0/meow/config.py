import json

class Config:
    conf = {}

    def __init__(self):
        with open('./config/config.json', 'r') as configFile:
            self.conf = json.load(configFile)

    def get(self, key):
        return self.conf[key]