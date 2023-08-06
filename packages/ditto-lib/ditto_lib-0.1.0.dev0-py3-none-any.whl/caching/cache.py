#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cache.py
#  Developed in 2018 by Hernan Gelaf-Romer <hernan_gelafromer@student.uml.edu>
#
#  Implements the basic cache mechanism for all ditto library
#

import time
import random
import sys
import threading
from pympler import asizeof

class Cache:

    def __init__(self, max_size, logger, timeout=None):
        self.__max_size = max_size
        self.__current_size = 0
        self.__cache = {}
        self.__logger = logger
        self.__timeout = timeout
        self.__lock = threading.Lock()
        self.__running = True
        self.__thread = None

    def __contains__(self, key):
        self.__lock.acquire()
        contains = key in self.__cache
        self.__lock.release()
        return contains

    def __len__(self):
        '''
        Return how many items are in the cache
        '''
        self.__lock.acquire()
        length = len(self.__cache)
        self.__lock.release()
        return length

    def __repr__(self):
        '''
        Show the internal cache
        '''
        return str(self.__cache)
    
    @property
    def size(self):
        '''
        Return the current size of the cache
        '''
        return self.__current_size

    @property
    def max_size(self):
        '''
        Return the capacity of the cache
        '''
        return self.__max_size

    @max_size.setter
    def max_size(self, max_size):
        '''
        Resize the cache, if you downsize, items may be 
        kicked out
        '''
        if max_size < self.__max_size:
            while self.__current_size > max_size:
                self._remove_oldest()
        self.__max_size = max_size
        self.__logger.log('debug', "Cache resized to {}".format(max_size))

    def _generate_cache_dict(self, value):
        '''
        Generate the dictionary that will be stored in the 
        cache with the given value
        '''
        return {'date_accessed' : time.time(),
            'value' : value, 'size' : asizeof.asizeof(value)}

    def add_item(self, key, value):
        '''
        Add an item to the current cache, removes the oldest 
        item if the cache now exceeds its maximum limit
        '''
        if asizeof.asizeof(value) >= self.__max_size:
            self.__logger.log('warn', "Tried to add object {} that was too large for the cache".format(key))
        else:
            if key in self:
                self.update_item(key, value)
            else:
                self.__lock.acquire()
                self.__cache[key] = self._generate_cache_dict(value)
                self.__logger.log('info', "Added {} to cache".format(key))
                self.__current_size += self.__cache[key]['size']
                self.__lock.release()
                while self.__current_size >= self.__max_size:
                    self._remove_oldest()

    def update_item(self, key, value):
        '''
        Update item with the key value pair given. Update time accessed to current 
        time and update the value to be what is given. Update the cache size according
        to the new size of the value
        '''
        if key not in self:
            self.__logger.log('warn', "{} not found in cache, adding".format(key))
            self.add_item(key, value)
        else:
            self.__lock.acquire()
            self.__current_size -= self.__cache[key]['size']
            self.__cache[key] = self._generate_cache_dict(value)
            self.__current_size += self.__cache[key]['size']
            self.__logger.log('debug', "Updated item {} in cache".format(key))
            self.__lock.release()
            while self.__current_size >= self.__max_size:
                self._remove_oldest()

    def get(self, key):
        '''
        Return the value associated with the given key. If the key is not in the
        cache, return None. If it is, update the accessed time of the cache with
        the current time
        '''
        if key not in self:
            self.__logger.log('warn', "Could not find value for {} in cache".format(key))
            return None
        else:
            self.__lock.acquire()
            value = self.__cache[key]['value']
            self.__cache[key]['date_accessed'] = time.time()
            self.__lock.release()
            self.__logger.log('info', "Retrieved {} from cache".format(key))
            return value

    def invalidate(self, key):
        '''
        Remove the key value pair associated with the given key 
        from the cache
        '''
        if key not in self:
            self.__logger.log('warn', "Could not find value for {} in cache".format(key))
        else:
            self.__lock.acquire()
            self.__current_size -= self.__cache[key]['size']
            del self.__cache[key]
            self.__logger.log('info', "Deleted {} from cache".format(key))
            self.__lock.release()

    def _remove_oldest(self):
        '''
        Remove the item in the cache that has gone the longest
        without be accessed 
        '''
        oldest_item = None
        self.__lock.acquire()
        for key, value in self.__cache.items():
            if oldest_item is None or value['date_accessed'] < self.__cache[oldest_item]['date_accessed']:
                oldest_item = key
        self.__lock.release()
        if oldest_item is None:
            self.__logger.log('warn', "Could not find item to remove from cache")
        else:
            self.invalidate(oldest_item)

    def __cleanup(self):
        '''
        Cleanup the cache periodically based on the set timeout
        '''
        while self.__running:
            self.__logger.log('info', "Running cleanup thread")
            current_time = time.time()
            to_delete = []
            self.__lock.acquire()
            for key, value in self.__cache.items():
                if current_time - value['date_accessed'] >= self.__timeout:
                    to_delete.append(key)
            self.__lock.release()
            for key in to_delete : self.invalidate(key)
            time.sleep(self.__timeout)
        