import os
import json
import time
import subprocess
import shlex
import psutil
import definitions
import importlib
from abc import ABCMeta, abstractmethod
from threading import Thread, Event
from collections import OrderedDict
from archiver.archiver import Archiver

class Collector(object):
    __metaclass__ = ABCMeta

    def factory(collector_config):
        collector_name = collector_config.get_collector_name()
        import_name = definitions.PLUGIN_DIRNAME +  "." + definitions.PLUGIN_COLLECTORS_DIRNAME + \
                      "." + collector_config.foldername + "." + collector_name
        mod = importlib.import_module(import_name)
        class_ = getattr(mod, collector_name)
        return class_(collector_config)

        # TODO: Clean this up
        # collector_type = collector_config.get_collector_type().lower()
        # if collector_type == "manual": ManualCollector(collector_config)
        # if collector_type == "automatic": AutomaticCollector(collector_config)
        # assert 0, "Bad collector creation: " + collector_type
        # return { #TODO: check if this is better
        #     "manual": ManualCollector(collector_config),
        #     "automatic": AutomaticCollector(collector_config)
        # }[collector_config.get_collecget_collector_archiving_time_intervaltor_type().lower()]
    factory = staticmethod(factory)

    def __init__(self, collector_config):
        self.config = collector_config
        self.name = self.config.get_collector_name()

        self.action = definitions.Action.RUN

        self.base_dir = os.path.join(definitions.PLUGIN_COLLECTORS_DIR, self.config.foldername)
        self.output_dir = os.path.join(self.base_dir, definitions.PLUGIN_COLLECTORS_OUTPUT_DIRNAME)
        self.parsed_dir = os.path.join(self.base_dir, definitions.PLUGIN_COLLECTORS_PARSED_DIRNAME)
        self.output_metadata_dir = os.path.join(self.output_dir, definitions.PLUGIN_COLLECTORS_METADATA_DIRNAME)

        self.devnull = open(os.devnull,'w')

        self.commands = []
        self.output_filenames = []
        self.processes = []
        self.pid_commands = {}

        self.refresh_data()

    def refresh_data(self):
        self.config.refresh_data()

        if self.config.collector_has_parser():
            parser_type = self.config.get_collector_parser()
            parser_type_tokens = parser_type.split(",")
            if len(parser_type_tokens) == 2:
                parser = getattr(__import__(
                    parser_type_tokens[0], fromlist=[parser_type_tokens[1]]),
                    parser_type_tokens[1])
                self.parser = parser(self)

    @abstractmethod
    def build_commands(self):
        ''' To override: Needs to set self.commands and self.output_filenames '''
        pass

    def set_action(self,action):
        self.action = action

    def get_action(self):
        return self.action

    def run(self):
        if self.is_running():
            return

        print (" --> Running %s" % self.name)

        self.build_commands()
        self.start_time = str(int(time.time()))
        self.create_metafile()

        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

        for command in self.commands:
            self.output_filenames.append(definitions.TIMESTAMP_PLACEHOLDER)
            self.run_command(command)

        if self.processes:
            print (" [x] Started: %s - pId(s): %s" % (self.name, ', '.join(str(p.pid) for p in self.processes)))

    def run_command(self, command):
        runcmds = shlex.split(command.replace(definitions.TIMESTAMP_PLACEHOLDER, self.start_time))

        try:
            process = subprocess.Popen(runcmds,
                                       shell=False,
                                       cwd=self.base_dir,
                                       stdout=self.devnull,
                                       stderr=self.devnull)
        except OSError as err:
            print "Error attempting to run command in collector: %s | command: %s\n" % (self.name, command)
            print "System Error:", err
        else:
            self.processes.append(process)
            self.pid_commands[process.pid] = command

    #TODO: fix to write proper timestamp
    def create_metafile(self):
        if not os.path.exists(self.output_metadata_dir):
            os.mkdir(self.output_metadata_dir)

        metadata_filename = 'meta_' + str(self.start_time) + \
                            definitions.PLUGIN_COLLECTORS_METADATA_FILENAME_EXTENSION
        self.metadata_filepath = os.path.join(self.output_metadata_dir, metadata_filename)

        metadata_file = open(self.metadata_filepath, "a")
        os.chmod(self.metadata_filepath, 0755) #TODO: What's this for?

        metadata_file.write(self.name + "\n")
        metadata_file.write("===============================\n")
        metadata_file.write("Commands:")
        for command in self.commands:
            metadata_file.write(definitions.PLUGIN_COLLECTORS_METADATA_FILE_COMMAND_PREFIX + command + "\n")
        metadata_file.write("===============================\n")
        metadata_file.close()

    def terminate(self):
        if not self.is_running():
            print ("  ...%s processes already dead" % self.name)
            return

        tps = []
        for process in self.processes:
            if process:
                parent_pid = process.pid
                parent = psutil.Process(parent_pid)
                try:
                    for child in parent.children(recursive=True):
                        child.kill()
                    parent.kill()
                except Exception as e:
                    print (" !! %s: %s" % (self.name, e))
                else:
                    tps.append(process.pid)
        print (" [x] Terminated: %s - pId(s): %s" % (self.name, ', '.join(str(p) for p in tps)))

        self.commands = []
        self.output_filenames = []
        self.processes = []
        self.pid_commands.clear()

    def is_running(self): #TODO: Is this best way to test this?
        if self.processes:
            return True
        return False

    def enable(self):
        os.remove(os.path.join(self.base_dir, definitions.PLUGIN_DISABLED_FILENAME))

    def disable(self):
        open(os.path.join(self.base_dir, definitions.PLUGIN_DISABLED_FILENAME), 'a').close()

    def is_enabled(self):
        return not os.path.isfile(os.path.join(self.base_dir, definitions.PLUGIN_DISABLED_FILENAME))

class ManualCollector(Collector):
    def __init__(self, collector_config):
        super(ManualCollector, self).__init__(collector_config)

        self.command_description = "" # Needs to be overridden

#TODO: Reduce overlap between classes
class AutomaticCollector(Collector):
    def __init__(self, collector_config):
        super(AutomaticCollector, self).__init__(collector_config)

        self.compressed_dir = os.path.join(self.base_dir, definitions.PLUGIN_COLLECTORS_COMPRESSED_DIRNAME)

        self.commands = []
        self.output_filenames = []
        self.processes = []
        self.pid_commands = {}

        self.archiver = None

    def refresh_data(self):
        super(AutomaticCollector, self).refresh_data()

        if self.config.collector_has_archiver():
            self.archiver = Archiver(self)

    def run(self):
        if self.is_running():
            return

        print (" --> Running %s" % self.name)

        self.build_commands()
        self.start_time = str(int(time.time()))
        self.create_metafile()

        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

        for command in self.commands:
            self.output_filenames.append(definitions.TIMESTAMP_PLACEHOLDER)
            self.run_command(command)

        if self.config.get_collector_auto_restart_enabled():
            self.stopFlag = Event()
            ar_thread = self.AutoRestart(self, self.stopFlag)
            ar_thread.start()

    def run_command(self, command):
        runcmds = shlex.split(command.replace(definitions.TIMESTAMP_PLACEHOLDER, self.start_time))

        try:
            process = subprocess.Popen(runcmds,
                                       shell=False,
                                       cwd=self.base_dir,
                                       stdout=self.devnull,
                                       stderr=self.devnull)

        except OSError as err:
            print "Error attempting to run command in collector: %s | command: %s\n" % (self.name, command)
            print "System Error:", err
        else:
            self.processes.append(process)
            self.pid_commands[process.pid] = command
            print("[x] Started: %s -pID(s): %s" % (self.name,str(process.pid)))


    def terminate(self):
        if not self.is_running():
            print ("  ...%s processes already dead" % self.name)
            return

        tps = []
        for process in self.processes:
            if process:
                parent_pid = process.pid
                parent = psutil.Process(parent_pid)
                try:
                    for child in parent.children(recursive=True):
                        child.kill()
                    parent.kill()
                except Exception as e:
                    print (" !! %s: %s" % (self.name, e))
                else:
                    tps.append(process.pid)
        print (" [x] Terminated: %s - pId(s): %s" % (self.name, ', '.join(str(p) for p in tps)))

        self.commands = []
        self.output_filenames = []
        self.processes = []
        self.pid_commands.clear()

    def is_running(self): #TODO: Is this best way to test this?
        if self.processes:
            return True
        return False

    class AutoRestart(Thread): #TODO: Review this
        def __init__(self, outer, event):
            Thread.__init__(self)
            self.outer = outer
            self.stopped = event
            self.auto_restart_enabled = self.outer.config.get_collector_auto_restart_enabled()
            self.time_interval = self.outer.config.get_collector_auto_restart_time_interval()

        def run(self):
            while not self.stopped.wait(self.time_interval):
                procs = list(self.outer.processes)
                for process in procs:
                    poll_res = process.poll()
                    if poll_res is not None:
                        self.restart_process(process)

        def restart_process(self, dead_process):
            command = self.outer.pid_commands[dead_process.pid]
            self.outer.processes.remove(dead_process)
            del self.outer.pid_commands[dead_process.pid]
            if(self.auto_restart_enabled):
                print("Auto restart enabled for: " + self.outer.name)
                print("Auto restart interval: " + str(self.time_interval))
                print("Attempting to restart...")
            #print(" --> process %s died, attempting to restart..." % (dead_process.pid))
            #In the case of tshark, process restarts, but dies if interface is down; can't tell if it continues runningd
            self.outer.run_command(command)


class CollectorConfig():
    TRACE_DELIMITER = "|" # Delimiter for json key trace

    def __init__(self, foldername):
        self.foldername = foldername
        self.file_path = os.path.join(
            definitions.PLUGIN_COLLECTORS_DIR, foldername, definitions.PLUGIN_COLLECTORS_CONFIG_FILENAME)
        self.schema_file_path = os.path.join(
            definitions.PLUGIN_COLLECTORS_DIR, foldername, definitions.PLUGIN_COLLECTORS_CONFIG_SCHEMA_FILENAME)

        self.refresh_data()
        
    def refresh_data(self):
        #TODO: add try/catch to these
        with open(self.file_path) as data_file:
            self.data = json.load(data_file, object_pairs_hook=OrderedDict)
        with open(self.schema_file_path) as schema_data_file:
            self.schema_data = json.load(schema_data_file, object_pairs_hook=OrderedDict)

        config_key_count = self.__sum_keys(self.get_configs_data())
        schema_config_key_count = self.__sum_keys(self.get_schema_configs_data())
        if self.schema_has_config_constraints():
            schema_config_key_count -= self.__sum_keys(self.get_schema_configs_constraints()) + 1
        if config_key_count != schema_config_key_count:
            raise ValueError("Config and schema sizes don't match")

    def get_data(self):
        return self.data

    def get_schema_data(self):
        return self.schema_data
    
    def get_collector_name(self):
        return self.get_data()["collector"]["name"]
    
    def get_collector_type(self):
        return self.get_data()["collector"]["type"]

    def get_configs_data(self):
        return self.get_data()["collector"]["configurations"]

    def get_schema_configs_data(self):
        return self.get_schema_data()["collector"]["configurations"]

    def get_schema_configs_constraints(self):
        if not self.schema_has_config_constraints():
            return {}
        return self.get_schema_configs_data()["constraints"]

    def get_collector_auto_restart_enabled(self):
        return self.get_configs_data()["general"]["auto restart"]["enabled"]

    def get_collector_auto_restart_time_interval(self):
        return self.get_configs_data()["general"]["auto restart"]["time interval"]

    def get_collector_archiving_enabled(self):
        return self.get_configs_data()["archiving"]["enabled"]

    def get_collector_archiving_time_interval(self):
        return self.get_configs_data()["archiving"]["time interval"]

    def get_collector_archiving_file_format(self):
        return self.get_configs_data()["archiving"]["file format"]

    def get_collector_parser(self):
        return self.get_configs_data()["parsing"]["parser"]

    def get_collector_custom_data(self):
        return self.get_configs_data()["custom"]

    def schema_has_config_constraints(self):
        return "constraints" in self.get_schema_configs_data()

    def collector_has_parser(self):
        if "parsing" in self.get_configs_data():
            return "parser" in self.get_configs_data()["parsing"]
        return False

    def collector_has_archiver(self):
        return "archiving" in self.get_configs_data()

    def __sum_keys(self, d):
        return (0 if not isinstance(d, dict)
                else len(d) + sum(self.__sum_keys(v) for v in d.itervalues()))

    def set_configs_data_field(self, trace, value):
        indexes = ""
        for key in trace.split(self.TRACE_DELIMITER):
            indexes += "[\"" + key + "\"]"
        statement = "self.data[\"collector\"][\"configurations\"]" + indexes + " = " + str(value)
        exec (statement)

    def get_schema_configs_data_field(self, trace):
        indexes = ""
        for key in trace.split(self.TRACE_DELIMITER):
            indexes += "[\"" + key + "\"]"
        return eval("self.schema_data[\"collector\"][\"configurations\"]" + indexes)

    def save_data(self):
        with open(self.file_path, 'w') as outfile:
            json.dump(self.data, outfile, indent=2)
