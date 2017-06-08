import os
import definitions
from engine.collector import AutomaticCollector

class snoopy(AutomaticCollector):
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
