import os
import time
import shutil
import logging
import traceback
import subprocess
import definitions

from threading import Event
from threading import Thread
from _version import __version__
from archiver.zip_format import zip
from archiver.tar_format import tar
from archiver.archiver import Archiver
from collector import CollectorConfig, Collector

#TODO: Remove these todos?
#TODO: get rid of all the print statements, provide result objects if required back to the client
#TODO: Handle sigterm correctly, background running thread gets stuck.  Need to use terminate() before quit() or CRTL-C
class Engine(object):
    def __init__(self):
        self.collectors = []
        self.collectors_dir = definitions.PLUGIN_COLLECTORS_DIR

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
        #Printing available collectors
        for i, collector in enumerate(self.collectors):
            print "%d) %s" % (i, collector.name)

    #TODO: TEST, method from main_gui.py
    def close_all(self):
        for collector in self.collectors:
            if collector.is_enabled:
               collector.terminate()
        os._exit(0)

    #TODO: TEST, method from main_gui.py
    def delete_all(self):
        delete_script = "cleanCollectorData.bat" if os.name == "nt" else "cleanCollectorData.sh"
        print "Deleting all collector data...."
        self.logger.info("Deleting all collector data....")
        remove_cmd = os.path.join(os.path.join(os.getcwd(), "scripts"), delete_script)
        subprocess.call(remove_cmd)  # TODO: Change this to not call external script
        os._exit(0)

    def stopall_collectors(self):
        for collector in self.collectors:
            if collector.is_enabled():
                collector.terminate()

    #TODO: TEST, method from main_gui.py
    def parse_all(self):
        for collector in self.collectors:
            collector.parser.parse()
            print "Parsing " + collector.name
            self.logger.info("Parsing " + collector.name)

    #TODO: TEST, method from main_gui.py
    def parser(self, collector):
        collector.parser.parse()

    #TODO: TEST, method from main_gui.py
    def startIndividualCollector(self, collector):
        collector.run()

    #TODO: TEST, mehtod from main_gui.py
    def startall_collectors(self):
        for collector in self.collectors:
            if collector.is_enabled() and isinstance(collector, collector.AutomaticCollector):
                print "Starting: ", collector
                self.logger.info("Starting: ", collector)
                collector.run()

    def stopIndividualCollector(self, collector):
        collector.terminate()

    #TODO: TEST
    def export(self):
        export_base_dir = '/root/Documents/ecel/'
        export_raw = True
        export_compressed = True
        export_parsed = True
        compress_export = True
        compress_export_format = 'zip'

        if export_base_dir == '':
            print "Please select a directory to export to."
            self.logger.info("Please select a directory to export to.")
            return
        if not os.path.isdir(export_base_dir):
            print "Please select a valid directory to export to."
            self.logger.info("Please select a valid directory to export to.")
            return
        if not export_raw and not export_compressed and not export_parsed:
            print "Please select at least one data type to export."
            self.logger.info("Please select at least one data type to export.")
            return

        export_dir = os.path.join(export_base_dir, definitions.PLUGIN_COLLECTORS_EXPORT_DIRNAME.replace(
            definitions.TIMESTAMP_PLACEHOLDER, "_" + str(int(time.time()))))
        export_raw_dir = os.path.join(export_dir, definitions.PLUGIN_COLLECTORS_OUTPUT_DIRNAME)
        export_compressed_dir = os.path.join(export_dir, definitions.PLUGIN_COLLECTORS_COMPRESSED_DIRNAME)
        export_parsed_dir = os.path.join(export_dir, definitions.PLUGIN_COLLECTORS_PARSED_DIRNAME)
        os.makedirs(export_raw_dir)
        os.makedirs(export_compressed_dir)
        os.makedirs(export_parsed_dir)

        for plugin in next(os.walk(self.collectors_dir))[1]:
            plugin_export_raw_dir = os.path.join(export_raw_dir, plugin)
            plugin_export_compressed_dir = os.path.join(export_compressed_dir, plugin)
            plugin_export_parsed_dir = os.path.join(export_parsed_dir, plugin)
            plugin_collector_dir = os.path.join(self.collectors_dir, plugin)
            plugin_collector_raw_dir = os.path.join(plugin_collector_dir, definitions.PLUGIN_COLLECTORS_OUTPUT_DIRNAME)
            plugin_collector_compressed_dir = os.path.join(plugin_collector_dir, definitions.PLUGIN_COLLECTORS_COMPRESSED_DIRNAME)
            plugin_collector_parsed_dir = os.path.join(plugin_collector_dir, definitions.PLUGIN_COLLECTORS_PARSED_DIRNAME)

            if export_raw and os.path.exists(plugin_collector_raw_dir) and os.listdir(plugin_collector_raw_dir):
                shutil.copytree(plugin_collector_raw_dir, plugin_export_raw_dir)
            if export_compressed and os.path.exists(plugin_collector_compressed_dir) and os.listdir(plugin_collector_compressed_dir):
                shutil.copytree(plugin_collector_compressed_dir, plugin_export_compressed_dir)
            if export_parsed and os.path.exists(plugin_collector_parsed_dir) and os.listdir(plugin_collector_parsed_dir):
                shutil.copytree(plugin_collector_parsed_dir, plugin_export_parsed_dir)
            print "Copying files " + plugin
            self.logger.info("Copying files " + plugin)

        #Compress export just checks what way to export zip or tar
        if compress_export:
            export_dir_notime = os.path.join(export_base_dir, definitions.PLUGIN_COLLECTORS_EXPORT_DIRNAME.replace(
                definitions.TIMESTAMP_PLACEHOLDER, ""))

            print "Compressing data to " + export_dir
            self.logger.info("Compressing data to " + export_dir)

            if compress_export_format == 'zip':
                zip(export_dir, export_dir_notime)
                print "Cleaning up " + export_dir
                self.logger.info("Cleaning up " + export_dir)
                print "Export complete"
                self.logger.info("Export complete")
            elif compress_export_format == 'tar':
                tar(export_dir, export_dir_notime)
                print "Cleaning up " + export_dir
                self.logger.info("Cleaning up " + export_dir)
                print "Export complete"
                self.logger.info("Export complete")
            else:
                print "Incorrect Compression type"
                self.logger.info("Incorrect Compression type")
                print "Export complete"
                self.logger.info("Export complete")

    def get_collector(self, name):
        return next(p for p in self.collectors if p.name == name)

    def get_collector_length(self):
        return self.collectors.__len__()

    def has_collectors_running(self):
        for collector in self.collectors:
            if(collector.is_running()):
                return True
        return False

    def list_collectors(self):
        for i, collector in enumerate(self.collectors):
            print "%d) %s" % (i, collector.name)
            self.logger.info("%d) %s" % (i, collector.name))
