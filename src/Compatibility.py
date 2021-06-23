class Compatibility():

    def dir_ftp_to_windows(dir):
        return dir.replace("/", "\\")

    def dir_windows_to_ftp(dir):
        return dir.replace("\\", "/")