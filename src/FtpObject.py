from src.Compatibility import Compatibility as c
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
        self.files = []

        self.create_dir_backup()
        self.tree(self.root)

    def create_dir_backup(self):
        if not self.config["name_backup"] in self.ftp.nlst():
            self.ftp.mkd(self.config["name_backup"])

    def tree(self, dir):
        try:
            for item in self.ftp.nlst(dir):
                if "." in item: # Exclude files
                    self.files.append(item[len(self.config["name_backup"])+1:])
                else:
                    self.directory.append(item[len(self.config["name_backup"])+2:])
                    self.tree(item)
        except ftplib.error_perm as e:
            print(e)

    def dir_push(self, parent, dir):
        self.ftp.cwd("/%s/%s" % (self.config["name_backup"], parent)) # Moove to parent dir
        self.ftp.mkd(dir) # Create directory
        print("[Dir Push] /%s/%s%s" % (self.config["name_backup"], parent, dir))

    def dir_del(self, parent, dir):
        try:
            self.ftp.cwd("/%s/%s" % (self.config["name_backup"], parent)) # Moove to parent dir
            self.ftp.rmd(dir) # Delete directory
            print("[Dir Delete] /%s/%s%s" % (self.config["name_backup"], parent, dir))
        except ftplib.error_perm as e:
            if str(e).find("Directory not empty") != -1:
                # Temp fonction
                print("[Error] Le repertoire %s%s n'est pas vide" % (parent, dir))
            else:
                print(e)

    def file_push(self, dir, file):

        with open("%s%s%s" % (self.config["dir_backup"], dir, file), "rb") as file_to_push:
            dir = c.dir_windows_to_ftp(dir)
            self.ftp.cwd("%s%s" % (self.root[:-1], dir))
            self.ftp.storbinary('STOR ' + file, file_to_push)

        print("[File Push] %s%s%s" % (self.config["dir_backup"], dir, file))

    def file_del(self, dir, file):
        self.ftp.cwd("%s%s" % (self.root, dir))
        self.ftp.delete(file)