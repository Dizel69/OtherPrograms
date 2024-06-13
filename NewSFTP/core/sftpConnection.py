import logging
import shutil
from os import listdir
import pysftp


# Это класс, который реализует общую логику для классов SftpServer и LocalFileServer.
class FileServerBase:
    def __init__(self, root_dir, server_type):
        self.root_dir = root_dir
        self.type = server_type

    def files(self):
        raise NotImplementedError

    def download(self, filename, local_file, remote_file, errors):
        logging.info("Downloading " + str(self.root_dir + remote_file) + " ...")
        try:
            self._download_impl(filename, local_file, remote_file)
        except (IOError, OSError):
            errors.append(filename)
            logging.exception("Can't load file from server " + str(self.server) + "," + filename)
            return False
        return True

    def _download_impl(self, filename, local_file, remote_file):
        raise NotImplementedError


# Этот класс наследует общий функционал от FileServerBase и
# реализует специфические методы для работы с SFTP.
class SftpServer(FileServerBase):
    def __init__(self, server, root_dir):
        super(SftpServer, self).__init__(root_dir, "sftp")
        self.server = server

    def files(self):
        return self.server.listdir(self.root_dir)

    def _download_impl(self, filename, local_file, remote_file):
        self.server.get(self.root_dir + remote_file, local_file)


# Этот класс также наследует общий функционал от FileServerBase
# и реализует специфические методы для работы с локальной файловой системой.
class LocalFileServer(FileServerBase):
    def __init__(self, root_dir):
        super(LocalFileServer, self).__init__(root_dir, "localfs")
        self.server = RServStub()

    def files(self):
        return listdir(self.root_dir)

    def _download_impl(self, filename, local_file, remote_file):
        file = self.root_dir + "/" + remote_file
        shutil.copyfile(file, local_file)


# Этот класс является заглушкой для сервера и содержит только один метод close.
class RServStub:
    def close(self):
        pass


# Настройка SFTP-соединения:
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None


# Эта функция создает параметры соединения, используя метод get,
# что позволяет избежать излишних проверок на наличие ключей
def create_sftp(sftp_config):
    parameters = {
        "host": sftp_config.get("host"),
        "username": sftp_config.get("userName"),
        "password": sftp_config.get("password"),
        "port": sftp_config.get("port"),
        "private_key": sftp_config.get("private_key"),
        "private_key_pass": sftp_config.get("private_key_pass"),
        "cnopts": cnopts
    }

    return SftpServer(pysftp.Connection(**parameters), sftp_config["rootDir"])
