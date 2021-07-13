import os

class LocalObject():
    
    def __init__(self, ftp_config):
        self.ftp_config = ftp_config
        self.directory = []
        self.files = []
        
        self.tree()

    def tree(self):
        for (directory, sousRepertoires, fichiers) in os.walk(self.ftp_config.backup_dir):
            if directory.find(".") == -1: # Exlude hidden folders
                # Save directory
                if len(directory) != len(self.ftp_config.backup_dir): # Exclude root dir
                    dir = directory[len(self.ftp_config.backup_dir):]
                    self.directory.append(dir.lstrip("\\"))
                # Save file
                for fichier in fichiers:
                    if fichier.find(".") != -1: # Exclude file without extension
                        file = "%s\\%s" % (directory[len(self.ftp_config.backup_dir):], fichier)
                        self.files.append(file.lstrip("\\"))

    def get_time(self, dir, file):
        return os.path.getmtime("%s/%s/%s" % (self.ftp_config.backup_dir, dir, file))
    
    def get_timestamp(self):
        return os.path.getmtime("timestamp.ts")