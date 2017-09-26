import os
import definitions
from engine.collector import AutomaticCollector
import shlex
import subprocess

class snoopy(AutomaticCollector):
    def snoopy_config_cmd(self, command):
        runcmd = shlex.split(command)

        try:
            subprocess.Popen(runcmd,
                             shell=False,
                             cwd=self.base_dir,
                             stdout=self.devnull,
                             stderr=self.devnull)

        except OSError as err:
            print "Error attempting to run command in collector: %s | command: %s\n" % (self.name, command)
            print "System Error:", err

    def build_commands(self):
        # get additional options from config.json
        self.snoopyLogPath = self.config.get_collector_custom_data()["log path"]

        # build commands
        out_file_name = definitions.TIMESTAMP_PLACEHOLDER + "_" + "snoopy"
        self.output_filenames.append(out_file_name)
        out_file_path = os.path.join(self.output_dir, out_file_name + ".txt")
        cmd = "./watchSnoopyFile.sh " \
            + str(self.snoopyLogPath) + " " \
            + str(out_file_path)

        self.commands.append(cmd)

#    def run(self):
        # additional logic to enable the snoopy library
#        self.snoopy_config_cmd("snoopy-enable")
        #now start the collector
#        super(snoopy, self).run()

#    def terminate(self):
#        #additional logic to disable the snoopy library
#        self.snoopy_config_cmd("snoopy-disable")
        #Now stop the collector
#        super(snoopy, self).terminate()

