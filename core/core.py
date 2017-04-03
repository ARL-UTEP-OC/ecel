import json
import os
import sys
import time
from threading import Event
from threading import Thread

import schedule

from Config import Runner
from archiver.Archiver import Archive
from plugin import PluginFactory

PLUGINS = "plugins"
COLLECTORS = "collectors"
PARSERS = "parsers"

# TODO: ger rid of all the print statements,
# provide result objects if required back to the client
# TODO: Handle sigterm correctly, background running thread
# gets stuck.  Need to use terminate() before quit() or CRTL-C
class Core(object):
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.config_file_path = os.path.join(self.dir_path, "config.json")
        self.plugins = []
        self.archivers = []
        self.parsers = {}

        Runner.scaffold_initial_files()

        # get core configurations
        with open(self.config_file_path) as config_file:
            self.config = json.load(config_file)

        # load all the plugin directory paths into a list
        self.plugins_directory = os.path.join(os.getcwd(), PLUGINS)
        self.collectors_directory = os.path.join(self.plugins_directory, COLLECTORS)
        self.parser_directory = os.path.join(self.plugins_directory, PARSERS)

        # Grab the core's archiver default settings
        self.archiverDefaults = self.config.get("Archiving")

        # Build plugin objects found in plugin directory
        plugin_factory = PluginFactory()

        for found_plugin_dir in os.listdir(self.collectors_directory):
            if not "__init__" in found_plugin_dir:
                plugin_base_dir = os.path.join(self.collectors_directory, found_plugin_dir)
                plugin = plugin_factory.build_from(plugin_base_dir)
                self.plugins.append(plugin)

                # TODO Check Parser with new
                if "Parser" in plugin.config:
                    parser_type = plugin.config["Parser"]["Value"]
                    parser_type_tokens = parser_type.split(",")
                    if len(parser_type_tokens) == 2:
                        parser = getattr(__import__(
                            parser_type_tokens[0], fromlist=[parser_type_tokens[1]]),
                            parser_type_tokens[1])

                        self.parsers[plugin.name] = parser(plugin)

                # Create the plugin's archiver
                if plugin.config_file.get("Archiving"):
                    plugin_arch_configs = plugin.config_file["Archiving"]
                    archiver = Archive(plugin, plugin_arch_configs)
                else:  # Plugin will use default core values
                    archiver = Archive(plugin, self.archiverDefaults)

                self.archivers.append(archiver)

        # TODO: this for sure, is no way to implement async stuff need to look into this
        self.wait_event = Event()
        self.stop_event = Event()
        self.thread = Thread(target=self.__update, args=(self.wait_event, self.stop_event,))
        self.thread.start()

    # TODO: update needs to be moved into the SchedulablePlugin class
    # there is no way to execute a SchedulablePlugin by itself if this is inside the core
    def __update(self, wait_event, stop_event):
        while not stop_event.is_set():
            wait_event.wait()
            schedule.run_pending()
            time.sleep(1)

    def get_plugin(self, name):
        return next(p for p in self.plugins if p.name == name)

    def run(self):
        # TODO: protect against calling multiple times
        # TODO: bad async stuff
        self.wait_event.set()
        for plugin in self.plugins:
            if plugin.is_enabled and not plugin.is_live():
                print ("Enabled: %s" % plugin.name)
                plugin.run()
            # TODO find a way to do it more efficiently
              #  for archive in self.archivers:
                   # if archive.plugin == plugin:
                        #archive.start()

    def list(self):
        self.wait_event.set()
        print "Plugins found:"
        i=1
        for plugin in self.plugins:
            print "  %d) %s" %(i , plugin.name)
            i += 1

    def suspend(self):
        self.wait_event.clear()
        for plugin in self.plugins:
            if plugin.is_enabled:
                plugin.suspend()

        for archive in self.archivers:
            archive.suspend()

    def resume(self):
        print "resume"
        self.wait_event.set()
        for plugin in self.plugins:
            if plugin.is_enabled:
                plugin.resume()

        for archive in self.archivers:
            archive.resume()

    def terminate(self):
        print "Terminating"
        # TODO: more bad async stuff
        self.stop_event.set()
        self.wait_event.set()

        for plugin in self.plugins:
            if plugin.is_enabled:
                plugin.terminate()

        for archive in self.archivers:
            print ("  ___ archiver terminated: %s" % archive.plugin.name)
            archive.stop()

        sys.exit()

    def parse(self):
        for plugin in self.plugins:
            self.parsers[plugin.name].parse()


    def decompress(self):
        self.suspend()              #Suspend plugin collectors from generating data

        for archive in self.archivers:
            #Calling decompress will suspend the archiver while decompressing. There's no need for suspending it here.
            #Actually, if is is suspended, the decompression will not work, because it checks it is enabled in order to execute.
            #archive.suspend()          #Stop archiver from archiving while decompression happens
            archive.decompress()    #Actual call to decompress
            print ("  Plugin Decompressed: %s" % archive.plugin.name)

    def get_enabled(self):
        print ("Enabled plugins:")
        i = 0
        for plugin in self.plugins:
            if plugin.is_enabled:
                i += 1
                print "%d) %s" % (i, plugin.name)
        print ("")
        if i == 0:
            print ("  No plugins are enabled\n")

    def get_running(self):
        print ("Running plugins:")
        i = 0
        for plugin in self.plugins:
            if plugin.is_running:
                i += 1
                print "%d) %s" % (i, plugin.name)
        if i == 0:
            print ("  No plugins are running\n")

def main(args):
    c = Core()
    c.run()
    time.sleep(10)
    c.terminate()

if __name__ == '__main__':
    main(sys.argv)