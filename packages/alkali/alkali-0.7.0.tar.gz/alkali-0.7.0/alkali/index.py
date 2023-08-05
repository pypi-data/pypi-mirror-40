import os
import json
import mmap

from .storage import Storage
from .filelock import FileLockMixin
from .peekorator import Peekorator
from .model import Model

import logging

logger = logging.getLogger(__name__)


class Index(FileLockMixin):
    """
    FIXME this is a file offset indexer, not a generic one
    need to handle generic key and generic value
    should Index.get(val) always return an entry? Should this
    be a member of the model or manager? Different owner depending
    on types? Gut says Manager...

    Similar api to a Query? Is Index a hybrid between Query and Storage?
    """

    def __init__(self, storage, f_index):
        """
        filename of index file
        """
        self._storage = storage
        self.f_index = f_index
        self.entries = {}

        super(Index, self).__init__(self.f_index.name())  # this locks the file
        logger.debug("creating index: %s", self.filename)

        # TODO read index if possible

        # FIXME requires file handle
        self.mmap = mmap.mmap(self._storage.filename, 0, access=mmap.ACCESS_READ)

    def get(self, key):
        """
        returns dict
        """
        start, finish = self.entries[key]

        data = self.mmap[start:finish]
        return self._storage.parse(data)

    def cb_pre_store(self, sender, instance, **kw):
        assert isinstance(instance, Storage)

    def cb_post_store(self, sender, instance, **kw):
        assert isinstance(instance, Storage)

        with open(self.filename, "w") as f:
            f.write("{\n")
            f.write('"filepath": "{}",\n'.format(instance.filename))
            f.write('"filesize": {},\n'.format(os.path.getsize(instance.filename)))
            f.write('"entries": [\n')

            _peek = Peekorator(self.entries.keys())
            for pk in _peek:
                pos = self.entries[pk]
                data = json.dumps({pk: pos})
                f.write(data)

                if not _peek.is_last():
                    f.write(",\n")

            f.write("\n]\n}")

    def cb_pre_store_instance(self, sender, instance, **kw):
        assert isinstance(instance, Model)

    def cb_post_store_instance(self, sender, instance, **kw):
        assert isinstance(instance, Model)
        self.entries[str(instance.pk)] = (kw["pos_start"], kw["pos_finish"])
