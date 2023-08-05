from __future__ import absolute_import

import datetime as dt
import os
import pickle
import sqlite3
import zlib

from appdirs import user_cache_dir

from .abc import DefaultMapping


class _DefaultSize(object):
    def __getitem__(self, _):
        return 1

    def __setitem__(self, _, value):
        assert value == 1

    def pop(self, _):
        return 1


class SQLite3Cache(DefaultMapping):
    """Mutable mapping to serve as a simple cache or cache base class."""

    __size = _DefaultSize()

    def __init__(self, maxsize, getsizeof=None, app_name="eidetic", version="0.1"):
        self.cache_dir = user_cache_dir(appname=app_name, version=version)
        self.cache_path = self.cache_dir + os.sep + "eidetic.db"

        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        self.con = sqlite3.connect(self.cache_path)
        self.c = self.con.cursor()

        self.c.execute(
            """CREATE TABLE IF NOT EXISTS cache
                          (key text primary key,
                          val blob not null,
                          timestamp datetime default current_timestamp
                          );"""
        )

        if getsizeof:
            self.getsizeof = getsizeof
        if self.getsizeof is not SQLite3Cache.getsizeof:
            self.__size = dict()
        self.__data = dict()
        self.__currsize = 0
        self.__maxsize = maxsize

    def __repr__(self):
        return "%s(%r, maxsize=%r, currsize=%r)" % (
            self.__class__.__name__,
            list(self.__data.items()),
            self.__maxsize,
            self.__currsize,
        )

    def __getitem__(self, key):
        try:
            return self.__data[key]
        except KeyError:
            # Check if it exists in the databse
            bresult = self.c.execute(
                "SELECT val from cache where key = ?", (key,)
            ).fetchone()
            if bresult is not None:
                decomp_result = zlib.decompress(bresult[0])
                pyresult = pickle.loads(decomp_result)
                self.__data[key] = pyresult
                return pyresult
            return self.__missing__(key)

    def __setitem__(self, key, value):
        maxsize = self.__maxsize
        size = self.getsizeof(value)
        if size > maxsize:
            raise ValueError("value too large")
        if key not in self.__data or self.__size[key] < size:
            while self.__currsize + size > maxsize:
                self.popitem()
        if key in self.__data:
            diffsize = size - self.__size[key]
        else:
            diffsize = size
        self.c.execute(
            "INSERT OR REPLACE INTO cache VALUES (?, ?, ?)",
            (key, zlib.compress(pickle.dumps(value), -1), dt.datetime.utcnow()),
        )
        self.con.commit()
        self.__data[key] = value
        self.__size[key] = size
        self.__currsize += diffsize

    def __delitem__(self, key):
        size = self.__size.pop(key)
        self.c.execute("DELETE FROM cache WHERE key = ?", (key,))
        self.con.commit()
        del self.__data[key]
        self.__currsize -= size

    def __contains__(self, key):
        return key in self.__data

    def __missing__(self, key):
        raise KeyError(key)

    def __iter__(self):
        return iter(self.__data)

    def __len__(self):
        return len(self.__data)

    @property
    def maxsize(self):
        """The maximum size of the cache."""
        return self.__maxsize

    @property
    def currsize(self):
        """The current size of the cache."""
        return self.__currsize

    @staticmethod
    def getsizeof(value):
        """Return the size of a cache element's value."""
        return 1
