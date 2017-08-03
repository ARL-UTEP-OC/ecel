import os
import netifaces
import definitions
from engine.collector import AutomaticCollector

class tshark(AutomaticCollector):
    #TODO: need plugin type in configs?

    #TODO: Use self.output_filepath?
    def build_commands(self):
        self.clean()
        # get additional options from the config file
        mode = self.config.get_collector_custom_data()["interfaces"]["mode"]
        ifaces = self.config.get_collector_custom_data()["interfaces"]["interfaces"]
        if mode == "inclusive":
            self.interfaces = ifaces
        else:
            self.interfaces = [iface for iface in netifaces.interfaces() if iface not in ifaces]

        # build commands
        for iface in self.interfaces:
            out_file_name = definitions.TIMESTAMP_PLACEHOLDER + "_" + iface
            self.output_filenames.append(out_file_name)
            out_file_path = os.path.join(self.output_dir, out_file_name + ".pcap")
            cmd = "dumpcap " \
                  + "-i " + str(iface) + " " \
                  + "-w " + str(out_file_path)
            self.commands.append(cmd)
