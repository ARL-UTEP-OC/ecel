#!/usr/bin/env python

import logging
from logging.handlers import SysLogHandler
import time
import sys
import os
from engine.engine import Engine
from service import find_syslog, Service

class ecel_Service(Service):

    def __init__(self, *args, **kwargs):
        self.collector = args[0].split('_', 3 )[-1:][0]
        super(ecel_Service, self).__init__(*args, **kwargs)
        self.logger.addHandler(SysLogHandler(address=find_syslog(),facility=SysLogHandler.LOG_DAEMON))
        self.logger.setLevel(logging.INFO)

    def run(self):
        print self.logger.info(self.collector)
        engine = Engine()
        collector = engine.get_collector(self.collector)
        print self.logger.info(collector)
        engine.startIndividualCollector(collector)
        while not self.got_sigterm():
            print self.logger.info("Running Collector...")

        if self.got_sigterm():
            print self.logger.info("Stopping all collectors and Exiting Program..")
            engine.stopIndividualCollector(collector)
            

if __name__ == '__main__':
    engine = Engine()

    collectors = engine.get_all_collectors()
    for i, collector in enumerate(collectors):
        if collector.name != 'manualscreenshot':
            service_name = "ecel_service_"+collector.name
            print "%s" % (collector.name)
            service = ecel_Service(service_name, pid_dir='/tmp')
            service.start()
    os._exit(0)
