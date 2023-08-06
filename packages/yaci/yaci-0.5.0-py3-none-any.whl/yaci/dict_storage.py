from __future__ import unicode_literals

from . import base_storage


class DictStorage(base_storage.CacheStorage):
    """
    Dictionary implementation of CacheStorage, stores
    values in memory. It should be noted that this is not truly
    a persistent cache, and that cache values will only last
    in the scope or context in which the cache was created. It is,
    suggested that you consider memoize should you need an in
    memory caching implementation.
    """

    def __init__(self):
        self._cache = dict()

    def get(self, key):
        """
        Return the value associated with key.

        :param key: Identifier used by storage implementaiton to retrieve value
        :raises KeyError: if value for key does not exist
        :returns: Object associated with key
        """
        return self._cache[key]

    def store(self, key, value):
        """
        Stores value using key as the lookup

        :param key: Identifier used by storage implementaiton to retrieve value
        :param value: Value to store associate with key
        :returns: None
        """
        self._cache[key] = value

    @property
    def size(self):
        """
        Returns the number of items cached.
        """
        return len(self._cache)

    def cached(self, key):
        """
        Return True if key is in cache False otherwise

        :param key: Identifier used by storage implementaiton to retrieve value
        """
        return key in self._cache

    def delete(self, key):
        """
        Deletes key and value associated with key from the storage

        :param key: Identifier used by storage implementaiton to retrieve value
        """
        del self._cache[key]

    def clear(self):
        """
        Remove the cache contents
        """
        self._cache = dict()

    def __iter__(self):
        return iter(self._cache)


class NoopDictStorage(DictStorage):
    """
    No-Op implementaiton of DictStorage. This implementation never
    stores any values, so the cache is always empty. NOTE: you will
    always encounter a CacheMiss exception when calling get.
    """

    def __init__(self):
        super(NoopDictStorage, self).__init__()

    def store(self, key, value):
        """
        No-Op storage. Does nothing.

        :param key: Identifier used by storage implementaiton to retrieve value
        :param value: Value to store associate with key
        :returns: None
        """
        pass

    def delete(self, key):
        """
        No-op deletion. Does nothing, because cache is always empty
        """
        pass
