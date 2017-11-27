#!/usr/bin/env python

import sys
import logging
import logging.handlers

from engine.engine import Engine

# Deafults
LOG_FILENAME = "/root/Documents/ECEL_Service.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

# create logger with 'ECEL'
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

# create file handler which logs even debug messages
fh = logging.FileHandler(LOG_FILENAME)
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
#logger.addHandler(ch)

logger.info('creating an instance of engine')
engine = Engine()
logger.info('created an instance of engine')
logger.info('calling engine.startIndividualCollector for tshark')
collector = engine.get_collector('tshark')
engine.startIndividualCollector(collector)
logger.info('finished starting engine.startIndividualCollector for tshark')
logger.info('stoping all collectors')
engine.close_all()
logger.info('done with engine')
