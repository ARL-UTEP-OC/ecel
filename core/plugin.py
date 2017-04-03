from threading import Thread, Event
import json
import os
import psutil
import subprocess
import time
import shlex
import schedule

# from plugins.collectors.tshark.module_tshark import TSharkPlugin

META_DIR_NAME = "META"  # Name given to the metafile directory
META_EXT = ".txt"  # Metafile extension
NO_ARGS_MSG = "(No args passed)"  # Message under args for the metafile

class PluginFactory(object):
    def build_from(self, base_dir):
        self.base_dir = base_dir
        self.config_file_path = os.path.join(base_dir, "config.json")
        self.config = None

        try:
            with open(self.config_file_path) as config_file:
                self.config_file = json.load(config_file)
                self.config = self.config_file.get("General")
                self.plugin_name = self.config.get("Plugin Name", {}).get("Value")
        except ValueError as e:
            print ("Config file is invalid: %s" % self.config_file_path)
            print e
        except Exception as e:
            print e

        if self.config != None:
            ctype = self.config["Type"]["Selected"]
            if ctype == Plugin.type:
                return Plugin(base_dir, self.config_file)
            elif ctype == SchedulablePlugin.type:
                return SchedulablePlugin(base_dir, self.config_file)
            elif ctype == ManualPlugin.type:
                return ManualPlugin(base_dir, self.config_file)
            elif ctype == 'custom':
                import_name = "plugins.collectors." + self.plugin_name + "." + self.plugin_name
                from_list = "plugins.collectors." + self.plugin_name
                mod = __import__(import_name, fromlist=from_list)
                class_ = getattr(mod, self.plugin_name)
                return class_(base_dir, self.config_file)
            else:
                raise ValueError("Type %s not found in plugin factory" % ctype)
        else:
            print ("The configurations from the JSON file could not be loaded: %s" % self.config_file_path)

###################################################################################
# provide result objects if required back to the client
class Plugin(object):
    __id = 0
    type = "plugin"
    def __init__(self, base_dir, config_file):

        self.processes = []
        self.cmds = []
        self.out_file_names = []
        self.metadata_filenames = []
        self.metadata_file_paths = []
        self.pid_cmds = {}
        self.devnull = open(os.devnull,'w')
        self.start_time = None

        # Required fields in all plugin config file are the following:
        # Plugin Name : Value
        # Is Enabled : Selected
        # Commands : Value
        # Auto Restart : Selected
        # Auto Restart Time Interval : Value

        ####REMOVED####
        # Exe Path : Value
        # Flags : Value
        # Output : Value
        # Extension : Selected
        # Is Standalone : Selected

        self.base_dir = base_dir
        self.config_file = config_file
        self.config = self.config_file.get("General")
        self.name = self.config.get("Plugin Name", {}).get("Value")
        self.is_enabled = self.config.get("Is Enabled", {}).get("Selected")
        commands = self.config.get("Commands", {}).get("Value")
        if commands:
            self.commands = commands.split(';')
        self.auto_restart = self.config.get("Auto Restart", {}).get("Selected")
        self.auto_restart_interval = int(self.config.get("Auto Restart Time Interval", {}).get("Value"))

        self.output_dir = os.path.join(base_dir, "raw")
        self.meta_dir = os.path.join(self.output_dir, META_DIR_NAME)

        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

        if self.auto_restart:
            self.stopFlag = Event()
            thread = self.AutoRestart(self, self.stopFlag)
            thread.start()

    def run(self):
        if self.is_enabled:
            if not self.is_live():
                self.build_cmds()
                self.start_time = str(int(time.time()))
                self.create_metafiles()

                for cmd in self.cmds:
                    self.run_cmd(cmd)

                if self.processes:
                    print (" --> Running %s" % self.name)
                    print (" [x] Starting: %s - pId(s): %s" % (self.name, ', '.join(str(p.pid) for p in self.processes)))
                    self.is_running = True

    def run_cmd(self, cmd):
        try:
            process = subprocess.Popen(shlex.split(cmd.replace("%TIME%", self.start_time)),
                                            shell=False,
                                            cwd=self.base_dir,
                                            stdout=self.devnull,
                                            stderr=self.devnull)
            self.processes.append(process)
            self.pid_cmds[process.pid] = cmd
            return process

        except Exception as err:
            print ("Error attempting to run command in plugin: %s | cmd: %s\n" % (self.name, cmd))
            print "System Error:", err

    def build_cmds(self):
        for command in self.commands:
            # Create output file for each command
            out_file_name = "%TIME%" # Time needed for metafile.
            self.out_file_names.append(out_file_name)
            cmd = str(command)
            self.cmds.append(cmd)

    def create_metafiles(self):
        for i, cmd in enumerate(self.cmds):
            if not os.path.exists(self.meta_dir):
                os.mkdir(self.meta_dir)
                os.path.join(self.meta_dir, "")

            metadata_filename = 'meta_' + str(self.out_file_names[i].replace("%TIME%", self.start_time)) + META_EXT
            self.metadata_filenames.append(metadata_filename)
            metadata_file_path = os.path.join(self.meta_dir, metadata_filename)
            self.metadata_file_paths.append(metadata_file_path)

            meta_file = open(metadata_file_path, "a")
            if os.name == "posix":
                os.chmod(metadata_file_path, 0755)
            meta_file.write(self.name + "\n===============================\n"
                            + "cmd= " + cmd)
            meta_file.close()

    def terminate(self):
        if not self.processes:
            print ("  ...%s processes already dead" % self.name)
            return
        tps = []
        for process in self.processes:
            if process:
                try:
                    parent_pid = process.pid
                    parent = psutil.Process(parent_pid)
                    for child in parent.children(recursive=True):  # or parent.children() for recursive=False
                        child.kill()
                    parent.kill()
                    tps.append(process.pid)
                except Exception as e:
                    print (" !! %s: %s" % (self.name, e))
        print (" [x] Terminating: %s - pId(s): %s" % (self.name, ', '.join(str(p) for p in tps)))
        # clear all lists
        self.processes = []
        self.cmds = []
        self.out_file_names = []
        self.metadata_filenames = []
        self.metadata_file_paths = []
        self.pid_cmds.clear()

    # TODO: implement status object, and job?! to collect status
    def is_live(self):
        if self.processes:
            return True
        return False

    def parse(self):
        if not self.is_live():
            return self.parser(self.base_dir).parse()
        else:
            return []
            # TODO: Detect changes to configuration elems (e.g. enabled) & reflect changes to Config file

        # def suspend(self):
        #     if self.is_running:
        #         for process in self.ps_processes:
        #             try:
        #                 process.suspend()
        #             except psutil.NoSuchProcess:
        #                 pass
        #         self.is_running = False

        # def resume(self):
        #     if not self.is_running:
        #         for process in self.ps_processes:
        #             try:
        #                 self.process.resume()
        #             except psutil.NoSuchProcess:
        #                 pass
        #         self.is_running = True

    class AutoRestart(Thread):
        def __init__(self, outer, event):
            Thread.__init__(self)
            self.outer = outer
            self.stopped = event

        def run(self):
            while not self.stopped.wait(self.outer.auto_restart_interval):
                procs = list(self.outer.processes)
                for process in procs:
                    poll_res = process.poll()
                    if poll_res is not None:
                        self.restart_process(process)

        def restart_process(self, dead_process):
            cmd = self.outer.pid_cmds[dead_process.pid]
            self.outer.processes.remove(dead_process)
            del self.outer.pid_cmds[dead_process.pid]
            print(" --> process %s died, attempting to restart..." % (dead_process.pid))
            #In the case of tshark, process restarts, but dies if interface is down; can't tell if it continues running
            self.outer.run_cmd(cmd)


###############################################################
#  plugin will not start on core.run()
class ManualPlugin(Plugin):
    type = "manual"

    def __init__(self, base_dir, config_file):
        super(ManualPlugin, self).__init__(base_dir, config_file)


###############################################################
class SchedulablePlugin(Plugin):
    type = "schedulable"

    def __init__(self, base_dir, config_file):
        # call super constructor
        super(SchedulablePlugin, self).__init__(base_dir, config_file)
        # TODO: we need to be able to define different scheduling schemes
        # see:  https://pypi.python.org/pypi/schedule
        # define structure in JSON we can then parse to define repetition
        # periods such seconds, minutes, etc...
        seconds = self.config.get("Schedule", {}).get("Value")
        seconds = int(seconds)
        # schedule.every(seconds).seconds.do(self.__run_process)  # TODO uncomment
        schedule.every(seconds).seconds.do(self.run)  # TODO uncomment


