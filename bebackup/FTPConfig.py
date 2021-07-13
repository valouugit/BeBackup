class FTPConfig():

    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.backup_dir = None
        self.backup_name = None