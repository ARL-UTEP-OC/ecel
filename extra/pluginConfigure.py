#pluginConfigure.py
#This class is designed to update the plugins that
#are within the program. The only fields that are being
#updated are status and output folder. Name will stay
#the same (as of 06/25) but we can add the option to change it.
#any other configurations for the plugin will have to be done manually
#and will be parsed to end of this file
#Last update: 06/25/16
#Last update by: John V.
import os
import json
import os.path


class configurePlugin(object):

    def __init__(self):
        #all of the fields needed in
        #a plugin config.json file
        self.plugin_name = ""
        self.plugin_status = ""
        self.plugin_fileformat = ""
        self.plugin_archiversize = ""
        self.plugin_sizeCheckPeriod = ""
        self.plugin_archiverTimeInterval = ""
        self.plugin_logsource = ""
        self.plugin_type = ""
        self.plugin_parser = ""
        #this is hard coded for the moment
        #just getting the output folder
        self.plugin_outfolder = os.path.dirname(os.path.realpath(__file__))
        #array that will store data from json file
        self.json_data = []
        self.load()

    #load the json Config file and use the first 3 elements
    #as the name, status and output folder
    def load(self):
        if os.path.exists('config.json'):
            with open('config.json') as data_file:
                self.json_data = json.load(data_file)
                self.set_status(self.json_data["enabled"])
                self.set_pluginparser(self.json_data["parser"])
                self.set_pluginname(self.json_data["name"])
                self.set_plugintype(self.json_data["type"])
                self.set_fileformat(self.json_data["archiver"]["fileFormat"])
                self.set_archiversize(self.json_data["archiver"]["archiverSize"])
                self.set_sizecheckperiod(self.json_data["archiver"]["sizeCheckPeriod"])
                self.set_archivertimeinterval(self.json_data["archiver"]["archiverTimeInterval"])
                command = raw_input("enter a command")
                self.get_command(command)
        else :
            print "Config file was not found, please ensure there is a config.json file"


    #gets user command
    #edits specific functions if user wants to
    def get_command(self, command):

        if command == "edit.name":
            newplugin_name = raw_input("enter a new name: ").lower()
            self.set_pluginname(newplugin_name)
            print "name updated"
            self.update_plugin()

        if command == "edit.status":
            newplugin_status = raw_input("enter enable or disable: ").lower()
            if newplugin_status == "enabled" or newplugin_status == "disabled":
                self.set_status(newplugin_status)
                print "status updated"
                self.update_plugin()
            else:
                print "Enable and Disable are the only options available. Please try again"

        if command == "edit.output":
            newplugin_folder = raw_input("enter a new output folder: ")
            self.set_outfolder(newplugin_folder)
            self.update_plugin()
        else :
            print "please enter a valid command"

    def get_name(self):
        return self.plugin_name

    def get_status(self):
        return self.plugin_status

    def get_outputfolder(self):
        return self.plugin_outfolder

    def get_fileformat(self):
        return self.plugin_fileformat

    def get_archiverSize(self):
        return self.plugin_archiversize

    def get_sizeCheckPeriod(self):
        return self.plugin_sizeCheckPeriod

    def get_archiverTimeInterval(self):
        return self.plugin_archiverTimeInterval

    def get_logSource(self):
        return self.plugin_logsource

    def get_type(self):
        return self.plugin_type

    def get_parser(self):
        return self.plugin_parser

    def set_pluginname(self, plugindata_name):
        self.plugin_name = plugindata_name

    def set_status(self, plugindata_status):
        self.plugin_status = plugindata_status

    def set_outfolder(self, plugindata_outfolder):
        self.plugin_outfolder = plugindata_outfolder

    def set_fileformat(self, plugindata_fileformat):
        self.plugin_fileformat = plugindata_fileformat

    def set_archiversize(self, plugindata_archiversize):
        self.plugin_archiversize = plugindata_archiversize

    def set_sizecheckperiod(self, plugindata_sizecheckperiod):
        self.plugin_sizeCheckPeriod = plugindata_sizecheckperiod

    def set_archivertimeinterval(self, plugindata_archivertimeinterval):
        self.plugin_archiverTimeInterval = plugindata_archivertimeinterval

    def set_logsource(self, plugindata_logsource):
        self.plugin_logsource = plugindata_logsource

    def set_plugintype(self, plugindata_type):
        self.plugin_type = plugindata_type

    def set_pluginparser(self, plugindata_parser):
        self.plugin_parser = plugindata_parser

    def update_plugin(self):
        jsonDictionary = {
            'Name' : self.get_name(),
            'enabled' : self.get_status(),
            'parser' : self.get_parser(),
            'type' : self.get_type(),
            "archiver" : {
                "fileFormat" : self.get_fileformat(),
                "archiverSize" : self.get_archiverSize(),
                "sizeCheckPeriod" : self.get_sizeCheckPeriod(),
                "archiverTimeInterval" : self.get_archiverTimeInterval()
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

test = configurePlugin()
