import json, os
from src.FileObject import FileObject

class LocalObject():
    
    def __init__(self):
        #   Load configuration
        with open("config.json", "r") as config:
            self.config = json.load(config)
        self.directory = []
        self.files = []
        
        self.__loading_files__()

    def __loading_files__(self):

        for (directory, sousRepertoires, fichiers) in os.walk(self.config["dir_backup"]):
            if directory.find(".") == -1: # Exlude hidden folders
                # Save directory
                self.directory.append(directory[len(self.config["dir_backup"])+1:])
                # Save file in FileObject
                for fichier in fichiers:
                    self.files.append(FileObject(directory, fichier))