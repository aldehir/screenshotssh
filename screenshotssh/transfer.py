from __future__ import print_function

import os
import posixpath

from paramiko.client import SSHClient
from paramiko.pkey import PKey

from .naming import generate_random_name


class TransferError(Exception):
    """Raised when a transfer error occurs."""


class TransferAgent(object):

    def __init__(self):
        self.client = SSHClient()
        self.client.load_system_host_keys()

        self.sftp_client = None

    def load_host_keys(self, filepath):
        self.client.load_host_keys(filepath)

    def connect(self, host, username=None, port=22, private_key_file=None):
        self.client.connect(host, username=username, port=port,
                                  key_filename=private_key_file)
        self.sftp_client = self.client.open_sftp()
        return self

    def close(self):
        self.sftp_client.close()
        self.client.close()

    def dest_file_exists(self, destpath):
        try:
            self.sftp_client.stat(destpath)
        except:
            return False

        return True

    def transfer(self, srcpath, destdir, callback=None, randomize=True,
                 name_length=7, max_attempts=4):
        if not randomize:
            destpath = self.transform_path(srcpath, destdir)
            return self.do_transfer(srcpath, destpath, callback=callback)

        for _ in range(max_attempts):
            name = generate_random_name(name_length)
            destpath = self.transform_path(srcpath, destdir, rename=name)

            if self.dest_file_exists(destpath):
                continue

            return self.do_transfer(srcpath, destpath, callback=callback)

        raise TransferError("Exceeded max transfer attempts")

    def do_transfer(self, src, dest, callback=None):
        self.sftp_client.put(src, dest, callback=callback)
        return dest

    def transform_path(self, srcpath, destdir, rename=None):
        basename = os.path.basename(srcpath)
        _, ext = os.path.splitext(basename)

        if rename:
            basename = rename + ext

        return posixpath.join(destdir, basename)
