from src.LocalObject import LocalObject
from src.FtpObject import FtpObject
from src.Compatibility import Compatibility as c

class SyncDirectory():

    def __init__(self, local, ftp):
        self.local = local
        self.ftp = ftp
        self.tree_sync = self.tree_compare()

    def tree_compare(self):
        
        tree_local = self.local.directory
        tree_ftp = self.ftp.directory
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



    