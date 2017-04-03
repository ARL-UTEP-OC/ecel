import json
import os.path

from Config.Model.Core.Default import Default


class CoreController:
    def __init__(self, base_dir, config_file_name):
        self.base_dir = base_dir
        self.config_file_name = config_file_name
        self.initialize_and_scaffold_config_files()

    def initialize_and_scaffold_config_files(self):
        if not os.path.isfile(self.plugins_config_file()):
            new_file = open(self.plugins_config_file(), 'w')

            data = Default().data

            with open(self.plugins_config_file(), 'w') as data_file:
                json.dump(data, data_file, sort_keys=True, indent=4, separators=(',', ': '))

            new_file.close()

    def plugins_config_file(self):
        return os.path.join(self.base_dir, 'core', self.config_file_name)
