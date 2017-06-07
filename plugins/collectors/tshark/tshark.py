import os
import netifaces
from engine.collector import AutomaticCollector

class tshark(AutomaticCollector):
    #TODO: need plugin type in configs?
    type = "tshark"
    command = "dumpcap"

    def __init__(self, collector_config):
        # call super constructor
        super(tshark, self).__init__(collector_config)
        # get additional options from the config file
        mode = collector_config.get_collector_custom_data()["interfaces"]["mode"]
        ifaces = collector_config.get_collector_custom_data()["interfaces"]["interfaces"]
        if mode == "inclusive":
            self.interfaces = ifaces
        else:
            self.interfaces = [iface for iface in netifaces.interfaces() if iface not in ifaces]

    def build_commands(self):
        for iface in self.interfaces:
            epoch_time = "%TIME%" #TODO: Use universal regex
            out_file_name = epoch_time + "_" + iface
            self.output_filenames.append(out_file_name)
            out_file_path = os.path.join(self.output_dir, out_file_name + ".pcap")
            cmd = self.command + " " \
                  + "-i " + str(iface) + " " \
                  + "-w " + str(out_file_path)
            self.commands.append(cmd)
