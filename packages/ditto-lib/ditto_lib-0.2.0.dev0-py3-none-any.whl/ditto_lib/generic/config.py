#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  config.py
#  Developed in 2018 by Hernan Gelaf-Romer <hernan_gelafromer@student.uml.edu>
#
#  Config file for all ditto_lib modules
#

from caching.cache import Cache
from colorlogging import ColorLogger

logger = ColorLogger(stream_level='info')
cache = Cache(max_size=1000000000, logger=logger, timeout=20) 