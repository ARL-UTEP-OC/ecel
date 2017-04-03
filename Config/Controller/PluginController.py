import json
import os.path

from Config.Model.Plugin.Default import Default
from Config.Model.Plugin.ManualScreenShot import ManualScreenShot
from Config.Model.Plugin.PyKeyLogger import PyKeyLogger
from Config.Model.Plugin.TShark import TShark
from Config.Model.Plugin.MultiIncTShark import MultiIncTShark
from Config.Model.Plugin.MultiExcTShark import MultiExcTShark
from Config.Model.Plugin.Snoopy import Snoopy


class PluginsController:
    def __init__(self, base_dir, config_file_name):
        self.base_dir = base_dir
        self.config_file_name = config_file_name
        self.plugin_names = [directory for directory in os.listdir(os.path.join(base_dir, 'plugins', 'collectors')) if
                             os.path.isdir(os.path.join(base_dir, 'plugins', 'collectors', directory))]

        self.initialize_and_scaffold_config_files()

    def initialize_and_scaffold_config_files(self):
        for plugin_name in self.plugin_names:
            if not os.path.isfile(self.plugins_config_file(plugin_name)):
                new_file = open(self.plugins_config_file(plugin_name), 'w')

                if plugin_name == 'manualscreenshot':
                    data = ManualScreenShot(plugin_name).data
                elif plugin_name == 'pykeylogger':
                    data = PyKeyLogger(plugin_name).data
                elif plugin_name == 'tshark':
                    data = TShark(plugin_name).data
                elif plugin_name == 'multi_inc_tshark':
                    data = MultiIncTShark(plugin_name).data
                elif plugin_name == 'multi_exc_tshark':
                    data = MultiExcTShark(plugin_name).data
                elif plugin_name == 'snoopy':
                    data = Snoopy(plugin_name).data
                else:
                    data = Default(plugin_name).data

                with open(self.plugins_config_file(plugin_name), 'w') as data_file:
                    json.dump(data, data_file, sort_keys=True, indent=4, separators=(',', ': '))

                new_file.close()

    def plugins_config_file(self, plugin_name):
        return os.path.join(self.base_dir, 'plugins', 'collectors', plugin_name, self.config_file_name)
