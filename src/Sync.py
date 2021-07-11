from src.Compatibility import Compatibility as c
from src.FtpObject import FtpObject
from src.LocalObject import LocalObject

class Sync():

    def __init__(self, log = True):
        self.log = log
        self.tree_resync()
        self.timestamp = self.diff_timestamp()

    def tree_resync(self):
        self.local = LocalObject()
        self.ftp = FtpObject(log = self.log)
        self.dir_tree_sync = self.tree_compare(self.local.directory, self.ftp.directory)
        self.files_tree_sync = self.tree_compare(self.local.files, self.ftp.files)

    def tree_compare(self, tree_local, tree_ftp):
        
        rest_dir_ftp = tree_ftp
        tree_sync = []

        for local in tree_local:
            local = c.dir_windows_to_ftp(local)
            sync = []
            sync.append(local)
            
            for ftp in tree_ftp:

                if local == ftp:
                    sync.append(ftp)
                    rest_dir_ftp.remove(ftp)

            if len(sync) == 1:
                sync.append("None")

            tree_sync.append(sync)

        for ftp in rest_dir_ftp:
            tree_sync.append(["None", ftp])

        return tree_sync

    def dir_sync(self, push = False, delete = False):
        
        def parse(here):
            dir = sync[here].split("/")
            dir = dir[len(dir)-1]
            parent = sync[0] if here==0 else sync[1]
            parent = parent[:-len(dir)]
            return dir, parent

        dir_tree_sync_order = self.dir_tree_sync
        if delete:
            dir_tree_sync_order.sort(key=lambda item:len(item[1]), reverse=True)
        else:
            dir_tree_sync_order.sort(key=lambda item:len(item[0]))

        for sync in dir_tree_sync_order:

            if sync[0] == "None" and delete:
                dir, parent = parse(1)
                try:
                    self.ftp.dir_del(parent, dir)
                except:
                    pass
            elif sync[1] == "None" and push:
                dir, parent = parse(0)
                self.ftp.dir_push(parent, dir)


    def files_sync(self, push = False, delete = False):
    
        def parse(here):
            files = sync[here].split("/")
            files = files[len(files)-1]
            dir = sync[0] if here==0 else sync[1]
            dir = dir[:-len(files)]
            return dir, files

        for sync in self.files_tree_sync:

            if sync[0] == "None" and delete:
                dir, files = parse(1)
                self.ftp.file_del(dir, files)
            elif sync[1] == "None" and push:
                dir, files = parse(0)
                self.ftp.file_push(c.dir_ftp_to_windows(dir), files) 
            elif sync[0] != "None" and sync[1] != "None" and push:
                dir, files = parse(0)
                if self.date_compare(dir, files):
                    self.ftp.file_push(c.dir_ftp_to_windows(dir), files)

    def date_compare(self, dir, file):
        time_local = self.local.get_time(dir, file) - self.timestamp
        time_ftp = self.ftp.get_time(dir, file)

        return True if time_local > time_ftp else False

    def diff_timestamp(self):
        file = "timestamp.ts"
        with open(file, "w") as ts:
            ts.write("timestamp")
        self.ftp.file_push(file="timestamp.ts", timestamp=True)
        time_local = self.local.get_timestamp()
        time_ftp = self.ftp.get_time("", file)

        return time_local - time_ftp

    def sync(self):
        if self.log: print("\nStarting backup\n")
        self.files_sync(delete=True)
        self.dir_sync(delete=True)
        self.dir_sync(push=True)
        self.files_sync(push=True)
        if self.log: print("\nBackup completed\n")
