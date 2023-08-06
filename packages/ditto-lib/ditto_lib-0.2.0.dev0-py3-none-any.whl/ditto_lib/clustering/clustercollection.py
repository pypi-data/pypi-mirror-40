#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# clustercollection.py
# Developed in 2018 by Hernan Gelaf-Romer <hernan_gelafromer@student.uml.edu>
#
# Implements the basic framework for a collection of clusters
#

from ditto_lib.generic.itemcollection import ItemCollection, logger
from ditto_lib.clustering.cluster import Cluster

from random import randint
from math import sqrt

class ClusterCollection(ItemCollection):
    '''
    Basic class for computing K-Mean clustering algorithm.\n
    Args:\n
    name: The name for the collection\n
    cluster_amount: The amount of clusters to group the items into. This
    defaults to 0. It is best to experiment and find the best value for this
    parameter. Some clustering alogrithms may override this input. 
    '''

    def __init__(self, name, cluster_amount=0):
        super(ClusterCollection, self).__init__(name)
        self._clusters = []
        self._cluster_amount = cluster_amount

    @property
    def cluster_amount(self):
        '''
        Return the amount of clusters, or centroid that this
        collection contains. 
        '''
        return self._cluster_amount

    @cluster_amount.setter
    def cluster_amount(self, cluster_amount):
        '''
        Set the amount of clusters, or centroids that this 
        collection contains
        '''
        self._cluster_amount = cluster_amount

    @property
    def clusters(self):
        '''
        Get all clusters associated with this collection
        '''
        return self._clusters

    def get_feature_ranking(self):
        '''
        Get a list of features in the order of importance. IE, the
        first item in the list will be the most impactful, and the least
        item in the list will be the least impactful in deciding where these
        items will be grouped
        '''
        pass

    def run_kmean(self, num_iterations=None):
        '''
        Run KMean algorithm. \n
        Args:\n
        items: The items that will be sorted into groups (clusters)\n
        num_iterations: Dicatate the amount of times that the algorithm
        will iterate through the data collection and assign items to clusters.
        If set to None (default value), the program will continue running until
        no more items move from one cluster to another
        '''
        self.__initialize_items_kmean()
        if num_iterations is not None:
            for i in range(num_iterations):
                self._calculate_cluster_averages()
                self._move_items()
                logger.log('info', "Completed iteration {}/{}".format(i + 1, num_iterations))
        else:
            while True:
                self._calculate_cluster_averages()
                if (self._move_items() is False):
                    break
        logger.log('info', "Done clustering by K-Mean algorithm")

    def _calculate_cluster_averages(self):
        '''
        Caclulate the average for all clusters
        '''
        for cluster in self._clusters:
            cluster.calculate_average()

    def _move_items(self):
        '''
        Move items to the cluster they are most similar to based
        on the euclidean distance. Returns whether an item was moved
        '''
        item_moved = False
        logger.log('debug', "Moving items")
        checked_items = set()
        for current_cluster_index, cluster in enumerate(self._clusters):
            for item in cluster.items:
                if item.name not in checked_items:
                    logger.log('debug', "Calculating appropriate cluster for {}".format(item.name))
                    # Find the best cluster for each item
                    best_cluster_index = 0
                    for cluster_index in range(self._cluster_amount):
                        if sqrt( (self._clusters[cluster_index].average - item.average)**2 ) < \
                                sqrt( (self._clusters[best_cluster_index].average - item.average)**2 ):
                            best_cluster_index = cluster_index
                    if best_cluster_index != current_cluster_index:
                        # Move item to appropriate cluster
                        self._clusters[current_cluster_index].remove_item(item)
                        self._clusters[best_cluster_index].add_item(item)
                        item_moved = True
                        logger.log('debug', "Item {} moved from Cluster Number {} to Cluster Number {}".format(
                            item.name, current_cluster_index, best_cluster_index))
                    checked_items.add(item.name)
        return item_moved

    def __initialize_items_kmean(self):
        self._clusters = []
        for i in range(self._cluster_amount):
            cluster = Cluster("Cluster Number {}".format(i))
            logger.log('info', "Cluster created {}".format(cluster.name))
            self._clusters.append(cluster)

        logger.log('debug', "Adding items to clusters at random")
        for item in self._items.values():
            self._clusters[randint(0, self._cluster_amount) - 1].add_item(item)
            item.calculate_average()
        logger.log('debug', "Finished adding items to clusters")
