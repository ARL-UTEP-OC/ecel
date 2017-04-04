import os
import time

from engine.plugin import Plugin


class snoopy(Plugin):
    type = "snoopy"
    command = ""

    def __init__(self, base_dir, config):
        # call super constructor
        super(snoopy, self).__init__(base_dir, config)
        # get additional options from config.json
        self.snoopyLogPath = self.config.get("Snoopy Log Path", {}).get("Value")

    def build_cmds(self):
        epoch_time = "%TIME%"
        out_file_name = epoch_time + "_" + "snoopy"
        self.out_file_names.append(out_file_name)
        out_file_path = os.path.join(self.output_dir, out_file_name + ".txt")
        cmd = "./watchSnoopyFile.sh " \
            + str(self.snoopyLogPath) + " " \
            + str(out_file_path)

        self.cmds.append(cmd)
