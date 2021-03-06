from .Compatibility import Compatibility as c
from ftplib import FTP
import ftplib, time

class FtpObject():

    def __init__(self, log = True, ftp_config = None):
        self.log = log
        self.ftp_config = ftp_config
        #   FTP connect
        self.ftp = FTP(self.ftp_config.hostname, self.ftp_config.username, self.ftp_config.password)
        self.root = "%s/%s/" % (self.ftp.pwd(), self.ftp_config.backup_name)
        self.directory = []
        self.files = []
        self.temp_directory = []
        self.temp_files = []

        self.create_dir_backup()
        self.tree(self.root)

    def create_dir_backup(self):
        if not self.ftp_config.backup_name in self.ftp.nlst():
            self.ftp.mkd(self.ftp_config.backup_name)

    def tree(self, dir, temp=False):
        try:
            for item in self.ftp.nlst(dir):
                if "." in item: # Exclude files
                    if temp:
                        self.temp_files.append(item.lstrip(self.root))
                    else:
                        self.files.append(item.lstrip(self.root))
                else:
                    if temp:
                        self.temp_directory.append(item.lstrip(self.root))
                        self.tree(item, temp=True)
                    else:
                        self.directory.append(item.lstrip(self.root))
                        self.tree(item)
        except ftplib.error_perm as e:
            print(e)

    def dir_push(self, parent, dir):
        self.ftp.cwd("/%s/%s" % (self.ftp_config.backup_name, parent)) # Moove to parent dir
        self.ftp.mkd(dir) # Create directory
        if self.log: print("Sending directory '%s%s'" % (parent, dir))

    def dir_del(self, parent, dir_del):
        try:
            self.ftp.cwd("/%s/%s" % (self.ftp_config.backup_name, parent)) # Moove to parent dir
            self.ftp.rmd(dir_del) # Delete directory
            if self.log: print("Deleting directory '%s%s'" % (parent, dir_del))
        except ftplib.error_perm as e:
            print(e)            

    def file_push(self, dir=None, file=None, timestamp=False):
        if not timestamp:
            with open("%s/%s/%s" % (self.ftp_config.backup_dir, dir, file), "rb") as file_to_push:
                dir = c.dir_windows_to_ftp(dir)
                self.ftp.cwd("/%s/%s" % (self.root, dir))
                self.ftp.storbinary('STOR ' + file, file_to_push)
                if self.log: print("Sending file '%s%s'" % (dir, file))
        else:
            with open(file, "rb") as file_to_push:
                self.ftp.cwd(self.root[:-1])
                self.ftp.storbinary('STOR ' + file, file_to_push)

    def file_del(self, dir, file):
        self.ftp.cwd("%s%s" % (self.root, dir))
        self.ftp.delete(file)
        if self.log: print("Deleting file '%s%s'" % (dir, file))

    def get_time(self, dir, file):
        self.ftp.cwd("%s%s" % (self.root, dir))
        datetime = self.ftp.voidcmd("MDTM " + file)[4:].strip()
        return time.mktime(time.strptime(datetime, '%Y%m%d%H%M%S'))