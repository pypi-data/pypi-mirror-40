import os
import types
import fcntl
from contextlib import contextmanager

# from zope.interface import Interface, Attribute, implements
import json
import csv

import logging

logger = logging.getLogger(__name__)


class FileAlreadyLocked(Exception):
    """
    the exception that is thrown when a storage instance tries
    and fails to lock its data file
    """

    pass


class FileLockMixin:
    """
    This mixin class accepts a filename/fhandle and locks it for
    exclusive access. Takes lock upon creation, releases at deletion.
    """

    def __init__(self, filename=None):
        self._fhandle = None
        self.filename = filename

    def __del__(self):
        self.unlock()

    @property
    def filename(self):
        if self._fhandle is None:
            return None

        return self._fhandle.name

    @filename.setter
    def filename(self, filename):
        """
        when setting the filename, immediately open and lock the file handle
        """
        self.unlock()

        if filename is None:
            if self._fhandle:
                self._fhandle.close()
                self._fhandle = None
            return

        if isinstance(filename, str):
            filename = os.path.expanduser(filename)

            if os.path.exists(filename):
                assert os.path.isfile(filename)
                self._fhandle = open(filename, "r+")
            else:
                self._fhandle = open(filename, "w+")

        else:  # assuming file type
            self._fhandle = filename

        self.lock()

    def lock(self):
        if not self._fhandle:
            return

        try:
            fcntl.flock(self._fhandle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError:
            raise FileAlreadyLocked("can't lock: {}".format(self.filename))

    def unlock(self):
        if not self._fhandle:
            return

        # I don't think this can ever fail
        fcntl.flock(self._fhandle, fcntl.LOCK_UN)
