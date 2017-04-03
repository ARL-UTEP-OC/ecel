#core configure . py
#This class is designed to update the core configurations
#that are set ffrom the user.
#
#
#
#
#
import os
import json

class configure_core(object):

    def __init__(self):
        self.core_name = ""
        self.plugin_folder = ""
        self.json_data = []
        self.load()

        # load the json Config file and use the first 3 elements
        # as the name, status and output folder

    def load(self):
        if os.path.exists('config.json'):
            with open('config.json') as data_file:
                self.json_data = json.load(data_file)
                self.set_status(self.json_data["enabled"])
                self.set_pluginparser(self.json_data["parser"])
                self.set_pluginname(self.json_data["name"])
                self.set_plugintype(self.json_data["type"])
                command = raw_input("enter a command")
                self.get_command(command)
        else:
            print "Config file was not found, please ensure there is a config.json file"

    # gets user command
    # edits specific functions if user wants to
    def get_command(self, command):
        if command == "edit.folder":
            newcore_pluginsfolder = raw_input("enter a new plugins folder: ")
            self.set_pluginsfolder(newcore_pluginsfolder)
            self.update_configuration()
        else:
            print "that is not a valid command, please try again"

    def get_pluginsfolder(self):
        return self.plugin_folder

    def set_pluginsfolder(self, plugin_folder):
        self.plugin_folder = plugin_folder

    def update_configuration(self):
        jsonDictionary = {
            "plugins" : {
                'directory': self.get_pluginsfolder()
            },
        }
        self.json_data.update(jsonDictionary)
        with open('config.json', 'w') as outfile:
            json.dump(self.json_data, outfile, sort_keys=True, indent=4)

    def destroy(self):
        ##just delete the Config file as we may not want to delete the entire plugin
        ##if the entire plugin is to be deleted, we use os.rmdir
        ##using the try to avoid having to us os.path.exists()
        try:
            os.remove('config.json')
        except OSError:
            pass

test = configure_core()