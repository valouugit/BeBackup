import json, os
from src.FileObject import FileObject

class LocalObject():
    
    def __init__(self):
        #   Load configuration
        with open("config.json", "r") as config:
            self.config = json.load(config)
        self.directory = []
        self.files = []
        