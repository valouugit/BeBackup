from src.Compatibility import Compatibility as c
from src.FtpObject import FtpObject
from src.LocalObject import LocalObject

class Sync():

    def __init__(self):
        self.local = LocalObject()
        self.ftp = FtpObject()
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
                sync.append(None)

            tree_sync.append(sync)

        for ftp in rest_dir_ftp:
            tree_sync.append([None, ftp])

        return tree_sync

    def dir_sync(self):
        
        def parse(here):
            dir = sync[here].split("/")
            dir = dir[len(dir)-1]
            parent = sync[0] if here==0 else sync[1]
            parent = parent[:-len(dir)]
            return dir, parent

        for sync in self.dir_tree_sync:

            if sync[0] == None:
                dir, parent = parse(1)
                self.ftp.dir_del(parent, dir)
            elif sync[1] == None:
                dir, parent = parse(0)
                self.ftp.dir_push(parent, dir)

    def files_sync(self):
    
        def parse(here):
            files = sync[here].split("/")
            files = files[len(files)-1]
            dir = sync[0] if here==0 else sync[1]
            dir = dir[:-len(files)]
            return dir, files

        for sync in self.files_tree_sync:

            if sync[0] == None:
                dir, files = parse(1)
                #self.ftp.dir_del(files, dir)
            elif sync[1] == None:
                dir, files = parse(0)
                self.ftp.file_push(c.dir_ftp_to_windows(dir), files) 