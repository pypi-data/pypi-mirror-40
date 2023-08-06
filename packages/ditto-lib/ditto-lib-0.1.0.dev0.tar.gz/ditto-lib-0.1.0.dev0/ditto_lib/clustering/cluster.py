#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# cluster.py
# Developed in 2018 by Hernan Gelaf-Romer <hernan_gelafromer@student.uml.edu>
#
# Implements a Cluster object 
#

from ditto_lib.generic.itemcollection import Item, logger

class Cluster():

    def __init__(self, name=None):
        self._name = name
        self._items = []
        self._average = 0

    def __repr__(self):
        return "Cluster name {} | Cluster average {}".format(self.name, self.average)

    @property
    def name(self):
        '''
        Name of the item
        '''
        return self._name

    @name.setter
    def name(self, name):
        logger.log('debug', "{} name set to {}".format(self._name, name))
        self._name = name

    @property
    def items(self):
        '''
        Return all the items stored by this cluster
        '''
        return self._items

    def add_item(self, item):
        self._items.append(item)
        logger.log('debug', "Added item {} from cluster {}".format(item.name, self.name))

    def remove_item(self, item):
        '''
        Remove the item from the items list
        '''
        self._items.remove(item)
        logger.log('debug', "Removed item {} from cluster {}".format(item.name, self.name))

    @property
    def average(self):
        '''
        Return the average of the current cluster based 
        on a kmean cluster approach
        '''
        return self._average

    def calculate_average(self):
        '''
        Caclulate the average of the current cluster based 
        on a kmean cluster approach
        '''
        self._average = 0
        if len(self._items) <= 0:
             logger.log('warn', "Cluster {} has no items associated with it".format(self.name))
        else:
            for item in self._items:
                for attribute in item.attributes.values():
                    self._average += attribute.value
            self._average /= len(self._items) * len(self._items[0].attributes)
        logger.log('debug', "Cluster {} average set to {}".format(self.name, self.average))
