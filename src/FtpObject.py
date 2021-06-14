from ftplib import FTP
import ftplib
import json, datetime, shutil, os

class FtpObject():

    def __init__(self):
        #   Load configuration
        with open("config.json", "r") as config:
            self.config = json.load(config)
        #   FTP connect
        self.ftp = FTP(self.config["ftp_server"], self.config["ftp_username"], self.config["ftp_password"])
        self.root = "%s/%s/" % (self.ftp.pwd(), self.config["name_backup"])
        self.directory = []

    def directory_tree(self, dir):
        try:
            for directory in self.ftp.nlst(dir):
                if directory.find(".") == -1: # Exclude files
                    self.directory.append(directory[len(self.config["name_backup"])+2:])
                    self.directory_tree(directory)
        except ftplib.error_perm as e:
            print(e)