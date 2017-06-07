import definitions
import os
from threading import Event
from threading import Thread

from archiver.archiver import Archiver
from collector import CollectorConfig, Collector

# TODO: get rid of all the print statements, provide result objects if required back to the client
# TODO: Handle sigterm correctly, background running thread gets stuck.  Need to use terminate() before quit() or CRTL-C
class Engine(object):
    def __init__(self):
        self.collectors = []

        collector_dirnames = [directory for directory in os.listdir(definitions.PLUGIN_COLLECTORS_DIR) if
                             os.path.isdir(os.path.join(definitions.PLUGIN_COLLECTORS_DIR, directory))]

        for collector_dirname in collector_dirnames:
            collector_config = CollectorConfig(collector_dirname) #TODO: Add try catch for this
            collector = Collector.factory(collector_config)
            self.collectors.append(collector)

            if collector_config.collector_has_parser():
                parser_type = collector_config.get_collector_parser()
                parser_type_tokens = parser_type.split(",")
                if len(parser_type_tokens) == 2:
                    parser = getattr(__import__(
                        parser_type_tokens[0], fromlist=[parser_type_tokens[1]]),
                        parser_type_tokens[1])
                    collector.parser = parser(collector)

            if collector_config.collector_has_archiver():
                archiver = Archiver(collector)
                collector.archiver = archiver

        #TODO: What's the point of this code?
        # TODO: this for sure is no way to implement async stuff need to look into this
        # self.wait_event = Event()
        # self.stop_event = Event()
        # self.thread = Thread(target=self.__update, args=(self.wait_event, self.stop_event,))
        # self.thread.start()

    def get_collector(self, name):
        return next(p for p in self.collectors if p.name == name)