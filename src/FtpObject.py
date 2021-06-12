from ftplib import FTP
import json, datetime, shutil, os

class FtpObject():

    def __init__(self):
        #   Chargement de la configuration
        with open("config.json", "r") as config:
            self.config = json.load(config)
        #   Connexion au server FTP
        self.ftp = FTP(self.config["ftp_server"], self.config["ftp_username"], self.config["ftp_password"])