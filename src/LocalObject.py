import json, os

class LocalObject():
    
    def __init__(self):
        #   Load configuration
        with open("config.json", "r") as config:
            self.config = json.load(config)
        self.directory = []
        self.files = []
        
        self.tree()

    def tree(self):
        for (directory, sousRepertoires, fichiers) in os.walk(self.config["dir_backup"]):
            if directory.find(".") == -1: # Exlude hidden folders
                # Save directory
                if len(directory) != len(self.config["dir_backup"]): # Exclude root dir
                    self.directory.append(directory[len(self.config["dir_backup"])+1:])
                # Save file
                for fichier in fichiers:
                    if fichier.find(".") != -1: # Exclude file without extension
                        file = "%s\\%s" % (directory[len(self.config["dir_backup"]):], fichier)
                        self.files.append(file.lstrip("\\"))

    def get_time(self, dir, file):
        return os.path.getmtime("%s/%s/%s" % (self.config["dir_backup"], dir, file))
    
    def get_timestamp(self):
        return os.path.getmtime("timestamp.ts")