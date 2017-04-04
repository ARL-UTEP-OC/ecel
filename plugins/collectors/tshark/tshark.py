import os
import time

from engine.plugin import Plugin


class tshark(Plugin):
    type = "tshark"
    command = "dumpcap"

    def __init__(self, base_dir, config):
        # call super constructor
        super(tshark, self).__init__(base_dir, config)
        # get additional options from config.json
        self.interface = self.config.get("Interface", {}).get("Value")

    def build_cmds(self):
        epoch_time = "%TIME%"
        out_file_name = epoch_time + "_" + self.interface
        self.out_file_names.append(out_file_name)
        out_file_path = os.path.join(self.output_dir, out_file_name + ".pcap")
        cmd = self.command + " " \
              + "-i " + str(self.interface) + " " \
              + "-w " + str(out_file_path)
        self.cmds.append(cmd)
