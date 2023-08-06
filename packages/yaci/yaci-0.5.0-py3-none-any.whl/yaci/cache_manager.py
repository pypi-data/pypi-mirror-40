"""
This module provides a caching interface that resembles a dictionary
The storage interface is expected to comply with the base_storage.CacheStorage
interface/abstraction.
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

try:
    from collections.abc import MutableMapping  # Python 3.x
except ImportError:
    from collections import MutableMapping  # Python 2.x


class CacheMissError(KeyError):
    """
    Exception for cache misses which is effectively a
    KeyError
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class CacheManager(MutableMapping):
    """
    The CacheManager class provides an abstraction for the implementation
    the persistent storage of objects via an interface that resembles a
    dictionary. The serialization/deserialization of objects is the responsibility
    of the particular storage interface. Storage implementations
    must conform to the abstraction set forth in base_storage.CacheStorage.
    """

    def __init__(self, storage=None):
        self._storage = storage

    def __getitem__(self, key):
        try:
            return self._storage.get(key)
        except KeyError:
            raise CacheMissError("No cache entry for %s" % key)

    def __setitem__(self, key, value):
        self._storage.store(key, value)

    def __contains__(self, key):
        return self._storage.cached(key)

    def __iter__(self):
        return iter(self._storage)

    def __delitem__(self, key):
        self._storage.delete(key)

    def __len__(self):
        return self._storage.size

    def clear(self):
        """
        Remove cache contents
        """
        self._storage.clear()

    def default_get(self, key, func, *args):
        """
        Return cache value if a cache key for value exists, otherwise,
        compute, store and return cache value.

        :param key:
        :param func: Function to use if value for key has not been cached
        :param *args: Arguments to be passed to value function.

        :return: Value associated with cache key.
        """
        value = None
        if not self._storage.cached(key):
            value = func(*args)
            self._storage.store(key, value)

        return self._storage.get(key) if self._storage.cached(key) else value

    @property
    def storage(self):
        """
        Storage implementation for cache.
        """
        return self._storage
