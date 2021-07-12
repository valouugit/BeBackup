from src.Sync import Sync
from src.FTPConfig import FTPConfig

print("""
  ██████╗ ███████╗██████╗  █████╗  ██████╗██╗  ██╗██╗   ██╗██████╗ 
  ██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██║   ██║██╔══██╗
  ██████╔╝█████╗  ██████╔╝███████║██║     █████╔╝ ██║   ██║██████╔╝
  ██╔══██╗██╔══╝  ██╔══██╗██╔══██║██║     ██╔═██╗ ██║   ██║██╔═══╝ 
  ██████╔╝███████╗██████╔╝██║  ██║╚██████╗██║  ██╗╚██████╔╝██║     
  ╚═════╝ ╚══════╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝""")


ftp_config = FTPConfig("hostname", "username", "password")

sync = Sync(ftp_config=ftp_config, backup_dir="C:\\Users\\user\\Documents\\", backup_name="BeBackup")
sync.sync()