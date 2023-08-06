#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  item.py
#  Developed in 2018 by Hernan Gelaf-Romer <hernan_gelafromer@student.uml.edu>
#
#  Implements the Data Point object that is used by the entire suite 
#

import uuid

from ditto_lib.generic.config import logger

class Item:

    def __init__(self, name):
        self.__id = uuid.uuid4()
        self.__hash = hash(name)
        self._name = name
        self._attributes = {}
        self._average = 0

    def __hash__(self):
        return self.__hash

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name == other.name \
            and self.attributes == other.attributes

    def __repr__(self):
        return "Item name {}".format(self.name)

    def size(self):
        '''
        Returns how many attributes pertain to this item
        '''
        return len(self.attributes)

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
    def attributes(self):
        '''
        Mapping of attribute name --> attribute class.
        Value will be None if not yet set
        '''
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        self._attributes = attributes

    def get_attribute(self, name):
        if name not in self._attributes:
            logger.log('error', "Could not get attribute {} from {}".format(name, self.name))
            return None
        else:
            return self._attributes[name]

    def get_attributes(self, attribute_names):
        '''
        Return list of attribute with given names
        '''
        attributes = []
        for name in attribute_names:
            current_attribute = self.get_attribute(name)
            if current_attribute:
                attributes.append(current_attribute)
        return attributes

    @property
    def id(self):
        '''
        Return the uuid of this item
        '''
        return self.__id

    def add_attribute(self, attribute):
        self._attributes[attribute.name] = attribute
        logger.log('debug', "Attribute {} with value {} added to Item {}".format(attribute.name, attribute.value, self.name))
    
    def remove_attribute(self, attribute):
        if attribute not in self.attributes:
            logger.log('error', "Could not remove {} because it doesn't exist in {}".format(attribute, self.name))
        else:
            del self.attributes[attribute]
    
    def copy(self):
        '''
        Return a deep copy of this item
        '''
        item = Item(self.name)
        for attribute in self.attributes.values():
            copy = attribute.copy()
            item.attributes[copy.name] = copy
        return item

    @property
    def average(self):
        '''
        Return the average value for all attributes. Useful 
        for clustering algorithsm
        '''
        return self._average

    def calculate_average(self):
        '''
        Caculate the average value for all attributes. Useful
        for clustering algorithms
        '''
        self._average = 0
        descriptors = 0
        for attribute in self._attributes.values():
            if attribute.is_descriptor is True:
                logger.log('debug', "Adding value {} to average".format(attribute.value))
                self._average += attribute.value
                descriptors += 1
        self._average /= descriptors
        logger.log('debug', "Item {} average calculated to be {}".format(
            self.name, self.average))