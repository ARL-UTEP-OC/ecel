import definitions
import os
import traceback
from threading import Event
from threading import Thread

from archiver.archiver import Archiver
from collector import CollectorConfig, Collector

#TODO: Remove these todos?
# TODO: get rid of all the print statements, provide result objects if required back to the client
# TODO: Handle sigterm correctly, background running thread gets stuck.  Need to use terminate() before quit() or CRTL-C
class Engine(object):
    def __init__(self):
        self.collectors = []

        collector_dirnames = [directory for directory in os.listdir(definitions.PLUGIN_COLLECTORS_DIR) if
                             os.path.isdir(os.path.join(definitions.PLUGIN_COLLECTORS_DIR, directory))]

        for collector_dirname in collector_dirnames:
            try:
                collector_config = CollectorConfig(collector_dirname)
            except ValueError:
                traceback.print_exc()
            else:
                collector = Collector.factory(collector_config)
                self.collectors.append(collector)

        #TODO: What's the point of this code? Remove?
        # TODO: this for sure is no way to implement async stuff need to look into this
        # self.wait_event = Event()
        # self.stop_event = Event()
        # self.thread = Thread(target=self.__update, args=(self.wait_event, self.stop_event,))
        # self.thread.start()

    def get_collector(self, name):
        return next(p for p in self.collectors if p.name == name)

    def get_collector_length(self):
        return self.collectors.__len__()