import os
import definitions
from engine.collector import AutomaticCollector

class nmap(AutomaticCollector):


    def build_commands(self):
        option = self.config.get_collector_custom_data()["interfaces"]["options"]
        network = self.config.get_collector_custom_data()["interfaces"]["network"]

        out_file_name = "nmap_" + definitions.TIMESTAMP_PLACEHOLDER
        self.output_filenames.append(out_file_name)
        out_file_path = os.path.join(self.output_dir, out_file_name + ".txt")

        # build commands
        cmd = self.name + option + network;
        self.commands.append(cmd)

