#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  utils.py
#  Developed in 2018 by Hernan Gelaf-Romer <hernan_gelafromer@student.uml.edu>
#
#  Basic utility functions for ditto_lib
#

from math import sqrt

def rmse(predictions, targets):
    score = 0
    counter = 0
    for prediction, target in zip(predictions, targets):
        score += sqrt((prediction - target) ** 2)
        counter += 1
    return score / counter

def percent_error(prediction, target):
    if (prediction == target):
        return 0
    else:
        return (min(prediction, target) / max(prediction, target)) * 100
