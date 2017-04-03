import os
import time
import netifaces

from core.plugin import Plugin


class multi_exc_tshark(Plugin):
    type = "multi_exc_tshark"
    command = "dumpcap"
    interfaces = []

    def __init__(self, base_dir, config):
        # call super constructor
        super(multi_exc_tshark, self).__init__(base_dir, config)
        # get additional options from config.json
        self.interfaces = self.config.get("Interfaces", {}).get("Value").split(',')
        # remove all whitespaces
        i = 0
        for i in range(0, len(self.interfaces)):
            self.interfaces[i] = self.interfaces[i].strip()

    def build_cmds(self):
        for iface in netifaces.interfaces():
            if iface.strip() not in self.interfaces:
                epoch_time = "%TIME%"
                out_file_name = epoch_time + "_" + iface
                self.out_file_names.append(out_file_name)
                out_file_path = os.path.join(self.output_dir, out_file_name + ".pcap")
                cmd = self.command + " " \
                      + "-i " + str(iface) + " " \
                      + "-w " + str(out_file_path)
                self.cmds.append(cmd)
