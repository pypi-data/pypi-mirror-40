"""
This module contains the abstraction for the
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import abc
import six  # For Python 2, Python 3 interoperability


@six.add_metaclass(abc.ABCMeta)
class CacheStorage():
    @abc.abstractmethod
    def store(self, key, value):
        """
        Cache the value associated with the cache_id
        :param cache_id: Identifier used by storage to locate value
        :param value: Data to be stored in cache
        """
        pass

    @abc.abstractmethod
    def get(self, key):
        """
        Return the the unique identifier used by the storage implementation
        to retrieve cache values.
        :param cache_id: Identifier used by storage to locate value
        """
        pass

    @abc.abstractmethod
    def cached(self, key):
        """
        Return if a value associated with the storage identifier exists
        in the storage implementation
        :param cache_id: Identifier used by storage to locate value
        """
        pass

    @abc.abstractproperty
    def size(self):
        """
        Return the integer size of the cache
        """
        pass

    @abc.abstractmethod
    def clear(self):
        """
        Remove the cache contents
        """
        pass

    @abc.abstractmethod
    def delete(self, key):
        """
        Deletes key and value associated with key from the storage

        :param key: Identifier used by storage implementaiton to retrieve value
        """
        pass
