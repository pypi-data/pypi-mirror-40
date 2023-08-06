#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  itemcollection.py
#  Developed in 2018 by Hernan Gelaf-Romer <hernan_gelafromer@student.uml.edu>
#
#  Implements the a container to store Data Point objects. This collection is cacheable
#

import csv
import os.path
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

from ditto_lib.generic.item import Item
from ditto_lib.generic.attribute import Attribute
from ditto_lib.generic.config import logger
from ditto_lib.generic.utils import percent_error, rmse, euclidean

class ItemCollection:

    def __init__(self, name):
        self._attributes = set()
        self._items = {}
        self._name = name
        
    @property
    def name(self):
        '''
        Name of the collection
        '''
        return self._name

    @name.setter
    def name(self, name):
        logger.log('debug', "{} name set to {}".format(self._name, name))
        self._name = name

    def __len__(self):
        '''
        Return how many items this collection is 
        storing
        '''
        return len(self._items)

    @property
    def attributes(self):
        '''
        Set of attribute names pertaining to this collection
        '''
        return self._attributes

    @property
    def items(self):
        '''
        Return all the dictionary of item name to items associated with this collection
        '''
        return self._items
    
    def get_item_objects(self):
        '''
        Return the list of all item objects instead of the 
        items dictionary
        '''
        return self._items.values()

    def get_item(self, name):
        '''
        Return the item object that has the given name. Returns None
        if the item was not found
        '''
        if name in self._items:
            return self._items[name]
        else:
            logger.log('error', "Could not get item {} from collection {}".format(name, self.name))
            raise ValueError("Could not get item {} from collection {}".format(name, self.name))

    def get_items(self, item_names):
        '''
        Return items that match the names given
        '''
        items = []
        for name in item_names:
            current_item = self.get_item(name)
            if current_item:
                items.append(current_item)
        return items

    def get_item_names(self):
        '''
        Return all the item names that are held by this 
        collection
        '''
        return self._items.keys()

    def add_attribute(self, attribute):
        '''
        Adds an attribute to the ItemCollection. Adds this 
        attribute to all the items within the collection as well
        '''
        self._attributes.add(attribute)
        logger.log('debug', "Added attribute {} to ItemCollection: {}".format(attribute, self._name))

        for item in self._items.values():
            if attribute not in item.attributes:
                item.add_attribute(Attribute(attribute))

    def remove_attribute(self, attribute):
        '''
        Remove the attribute from this collection and all items 
        stored in this collection as well
        '''
        if attribute not in self.attributes:
            logger.log('error', "Could not remove {} because it doesn't exist in {}".format(attribute, self.name))
        else:
            self.attributes.remove(attribute)
            for item in self.items.values():
                item.remove_attribute(attribute)

    def set_is_descriptor(self, attribute_names, is_descriptor):
        '''
        Set the list of given attributes' 'is_descriptor' value to the given boolean\n
        Args:\n
        attribute_names: An iterable collection of attribute names to modify\n
        is_descriptor: A boolean value describing whether the attribute is a descriptor or not
        '''
        for name in attribute_names:
            for item in self.items.values():
                if name in item.attributes:
                    item.get_attribute(name).is_descriptor = is_descriptor
                else:
                    logger.log('error', "Could not find attribute {} in collection {}".format(name, self.name))
    
    def add_item(self, item):
        '''
        Adds a item to the collection.
        '''
        self._items[item.name] = item
        for attribute in item.attributes.values():
            if attribute.name not in self.attributes:
                self.add_attribute(attribute.name)  

        for attribute in self.attributes:
            if attribute not in item.attributes:
                item.add_attribute(Attribute(attribute))         
        logger.log('info', "Added {} to ItemCollection: {}".format(item.name, self._name))

    def get_sorted(self, attribute_name, descending=False):
        '''
        Return a list of the data items sorted by the
        given attribute. Frames that don't have this attribute
        defined are sent to the back of the list
        '''

        if attribute_name in self._attributes:
            return sorted(self._items.values(), key=lambda item : (item.attributes[attribute_name].value is None,
                item.attributes[attribute_name].value), reverse=descending)
        else:
            logger.log('error', "Tried to sort by {} which does not exist in container {}".format(attribute_name, self._name))
            raise ValueError("Tried to sort by {} which does not exist in container {}".format(attribute_name, self._name))

    def merge_collections(self, collections, new_name):
        '''
        Return a collection that is the result of merging this
        collecition and the one that is given. Merge attributes 
        and Data Frames\n

        Args:\n
        collection: The list of collections to merge with this collection\n
        new_name: The name of the new collection
        '''

        # Merge the attributes from both collection
        new_attributes = self.attributes
        for collection in collections:
            new_attributes.update(collection.attributes)

        # Merge items from both collections
        new_items = self._items
        self._items.update(collection.items)

        # Create the new collection and fill it with items
        new_collection = ItemCollection(new_name)
        new_collection._attributes = new_attributes
        new_collection._items = new_items
        logger.log('info', "Merged {} with {}".format(self.name, \
            [collection.name for collection in collections]))
        return new_collection

    def copy(self, name):
        '''
        Return a deep copy of this collection with the name
        that is passed
        '''
        new_collection = ItemCollection(name)
        new_collection._attributes = set([attribute for attribute in self.attributes])
        for item in self.items.values():
            copy = item.copy()
            new_collection.items[copy.name] = copy
        logger.log('debug', "{} copied to {}".format(self.name, new_collection.name))
        return new_collection

    def wipe(self):
        '''
        Wipe the current ItemCollection. Resetting its ItemCollections and
        attributes. Will keep the same name
        '''
        self._items = {}
        self._attributes = set()

    def from_csv(self, filename, attribute_row=0, attribute_column=0, delimiter=',', encoding='utf-8-sig', non_descriptors=set(), cache_csv=True):
        '''
        Remove any data from this ItemCollection and import
        the data from a csv file

        Args:

        filename: The name of the csv file

        attribute_row: The row containing the name of the attributes. Defaults
        to 0. Anything under this will be assumed to be the values pertaining to 
        the current ItemCollection. This method assumes the first column of every row
        is the name of the current ItemCollection

        attribute_column: The column containing the start of where the attribute values 
        will be located. Defaults to 0

        delimiter: Delimiter that will be used, defaults to ','

        encoding: Encoding that will be used, defaults to 'utf-8-sig'
    
        non_descriptors: The set of names of any attributes that will not be descriptors in the 
        ItemCollection. Defaults to an empty set
        '''
        self.wipe()
        if '.csv' not in filename: 
            filename += '.csv'
        try:
            with open(filename, newline='') as file:
                data_raw = list(csv.reader(file))
        except FileNotFoundError:
            logger.log('error', "Could not find file {}".format(filename))
            raise FileNotFoundError("Couldn't find file {}".format(filename))

        # Import attributes
        for attribute_name in data_raw[attribute_row][attribute_column:]:
            self.attributes.add(attribute_name)
        logger.log('debug', "Attribut list generated {}".format([attribute for attribute in self.attributes]))

        # Import items
        for column in data_raw[attribute_row + 1:]:
            attributes = {}
            item = Item(column[0])
            logger.log('debug', "Adding item {} from csv".format(item.name))
            for index, attribute_name in enumerate(data_raw[attribute_row][attribute_column:]):
                attributes[attribute_name] = Attribute(attribute_name, column[index + attribute_column], 
                    attribute_name not in non_descriptors)
            item.attributes = attributes
            self.items[item.name] = item
        logger.log('info', "Imported {} from {}".format(self.name, filename))

    def to_csv(self, filename):
        '''
        Export this ItemCollection to the csv file given
        '''
        with open(filename, mode='w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            attributes_list = [attribute for attribute in self._attributes]
            csv_writer.writerow(['Name'] + attributes_list)
            for item in self.items.values():
                csv_writer.writerow([item.name] + 
                [item.attributes[attribute].value for attribute in attributes_list])
            logger.log('info', "{}  written to {}".format(self.name, filename))
    
    def scatter_plot(self, x_axis, y_axis, filename=None):
        '''
        Plot the current collection's items based on the attribute
        that is given
        '''
        if x_axis not in self._attributes:
            logger.log('error', "Could not plot based on attribute {} because it was not contained in {}".format(x_axis, self.name))
            raise ValueError("Could not plot based on attribute {} because it was not contained in {}".format(x_axis, self.name))
        elif y_axis not in self._attributes:
            logger.log('error', "Could not plot based on attribute {} because it was not contained in {}".format(y_axis, self.name))
            raise ValueError("Could not plot based on attribute {} because it was not contained in {}".format(y_axis, self.name))
        else:
            items = {}
            for item in self._items.values():
                items[item.name] = (item.attributes[x_axis].value, item.attributes[y_axis].value)
            x_coords = []
            y_coords = []

            for coord in items.values():
                x_coords.append(coord[0])
                y_coords.append(coord[1])

            plt.scatter(x_coords, y_coords, marker='o')
            plt.xlabel(x_axis)
            plt.ylabel(y_axis)
            
            if filename is not None:
                logger.log('info', "Saving scatter plot to {}".format(filename))
                plt.savefig(filename, bbox_inches='tight')
            else:
                logger.log('info', "Showing scatter plot")
                plt.show()

    def random_forest_classification(self, n_components, target_attribute, n_estimators=200):
        '''
        Return attributes of each item in the collection and
        in the order of their importance based on a random forest
        analysis.\n
        Args:\n
        n_components: The number of attributes returned in the list\n
        target_attribute: The target output value for each feature set input, should be a non
        descriptive attribute name\n
        n_estimators: The number of trees in a forest.
        '''
        logger.log('debug', "Running feature selection for {}".format(self.name))
        attributes = self._get_descriptive_attributes()
        data_raw = self._get_raw_data()
        target_values = [int(item.get_attribute(target_attribute).value) for item in self.items.values()]
        if len(target_values) != len(data_raw):
            logger.log('error', "Target values != Amount of input")
            raise ValueError("Target values != Amount of input")
        clf = RandomForestClassifier(n_estimators=n_estimators, oob_score=True, random_state=0)
        clf.fit(data_raw, target_values)
        final_data = []
        for index, attribute in enumerate(attributes):
            final_data.append((attribute.name, clf.feature_importances_[index]))
        final_data.sort(key=lambda x: x[1], reverse=True)
        logger.log('info', "Ran feature selection for {}".format(self.name))
        return final_data[:n_components]

    def calc_rmse(self, target_score, actual_score):
        '''
        Generate an rmse value\n
        Args:\n
        target_score: The name of the target score attribute\n
        actual_score: The name of the actual score attribute\n
        '''
        if target_score not in self.attributes or actual_score not in self.attributes:
            logger.log('error', "{} or {} not in collection {}".format(target_score, actual_score, self.name))
            raise ValueError("{} or {} not in collection {}".format(target_score, actual_score, self.name))
        target_scores = []
        actual_scores = []
        for item in self.items.values():
            target_scores.append(float(item.get_attribute(target_score).value))
            actual_scores.append(float(item.get_attribute(actual_score).value))
        return rmse(target_scores, actual_scores)
    
    def generate_error(self, name, target_score, actual_score):
        '''
        Generate the percent error of one attribute compared to another
        attribute for every item in the collection.\n
        Args:\n
        name: The name of the new attribute where the result will be stored\n
        target_score: The target score that will be compared to the actual score\n
        actual_score: The actual score that will be compared to the target score
        '''
        if target_score not in self.attributes or actual_score not in self.attributes:
            logger.log('error', "{} or {} not in collection {}".format(target_score, actual_score, self.name))
            raise ValueError("{} or {} not in collection {}".format(target_score, actual_score, self.name))
        self.attributes.add(name)
        for item in self.items.values():
            attribute = Attribute(name, is_descriptor=False)
            target = float(item.get_attribute(target_score).value)
            actual = float(item.get_attribute(actual_score).value)
            attribute.value = percent_error(actual, target)
            item.add_attribute(attribute)
            logger.log('debug', "Percent error: {}, found between target score {} and actual score {} for item {}".format(attribute.value,
                target_score, actual_score, item.name))

    def calculate_similarity(self, first_item, second_item):
        '''
        Calculate the similarity between two items in a collection
        '''
        if first_item not in self.items or second_item not in self.items:
            logger.log('error', "Could not find {} or {} in {}".format(first_item, second_item, self.name))
            raise ValueError("Could not find {} or {} in {}".format(first_item, second_item, self.name))
        else:
            first_item = self.get_item(first_item)
            second_item = self.get_item(second_item)
            first_values = []
            second_values = []
            for attribute in self.attributes:
                if first_item.get_attribute(attribute).is_descriptor:
                    first_values.append(first_item.get_attribute(attribute).value)
                    second_values.append(second_item.get_attribute(attribute).value)
            logger.log('debug', "first_values {}, second_values {}".format(first_values, second_values))
            return euclidean(first_values, second_values)

    def calculate_all_similarities(self, item):
        '''
        Return a list of tuples where the first value is the 
        item it is being compared to, and the second value is the
        similarity score between the two items
        '''
        item = self.get_item(item)
        results = []
        for other_item in self.items.values():
            if item != other_item:
                results.append((other_item.name, self.calculate_similarity(item.name, other_item.name)))
        return results

    def _get_descriptive_attributes(self):
        attributes = []
        for attribute in next(iter(self.items.values())).attributes.values():
            if attribute.is_descriptor:
                attributes.append(attribute)
        return attributes

    def _get_raw_data(self):
        data_raw = []
        for item in self.items.values():
            item_data = []
            for attribute in self.attributes:
                if item.get_attribute(attribute).is_descriptor:
                    item_data.append(item.get_attribute(attribute).value)
            data_raw.append(item_data)
        return data_raw