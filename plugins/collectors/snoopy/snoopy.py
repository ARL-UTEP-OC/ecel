import os
import time

from engine.collector import AutomaticCollector


class snoopy(AutomaticCollector):
    type = "snoopy"
    command = ""

    def __init__(self, collector_config):
        # call super constructor
        super(snoopy, self).__init__(collector_config)
        # get additional options from config.json
        self.snoopyLogPath = collector_config.get_collector_custom_data()["log path"]

    #TODO: Use self.output_filepath?
    def build_commands(self):
        epoch_time = "%TIME%"
        out_file_name = epoch_time + "_" + "snoopy"
        self.output_filenames.append(out_file_name)
        out_file_path = os.path.join(self.output_dir, out_file_name + ".txt")
        cmd = "./watchSnoopyFile.sh " \
            + str(self.snoopyLogPath) + " " \
            + str(out_file_path)

        self.commands.append(cmd)
