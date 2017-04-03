import json
import os.path
from Tkinter import *

import netifaces

from Config.View.Plugin.AddEntryView import AddEntryView
from Config.View.Plugin.AddOptionsView import AddOptionsView
from Config.View.Plugin.AddToBlacklistView import AddToBlacklistView
from Config.View.Plugin.RemoveConfigurationView import RemoveConfigurationView
from Config.View.Plugin.RemoveFromBlacklistView import RemoveFromBlacklistView


class MakeView:
    def __init__(self, root, base_dir, plugin_name, config_file_name):
        self.root = root
        self.base_dir = base_dir
        self.plugin_name = plugin_name
        self.config_file_name = config_file_name

        self.file_path = os.path.join(self.base_dir, 'plugins', 'collectors', self.plugin_name, self.config_file_name)

        self.general_entry_counter = 0
        self.general_option_counter = 0
        row_counter = 1
        self.general_label_labels = []
        self.general_labels = []
        self.general_entry_labels = []
        self.general_entries = []
        self.general_option_labels = []
        self.general_options = []

        general_settings_label = Label(root, text="General Settings")
        general_settings_label.grid(sticky="W", row=0, column=2)

        if os.path.isfile(self.file_path):
            with open(self.file_path) as data_file:
                self.data = json.load(data_file)

        for key, value in self.data['General'].iteritems():
            if value['Field Type'] == 'Entry':
                self.general_entry_labels.append(Label(root, text=key))
                self.general_entry_labels[self.general_entry_counter].grid(sticky="W", row=row_counter, column=1)

                self.general_entries.append(Entry(root))
                self.general_entries[self.general_entry_counter].insert(0, value['Value'])
                self.general_entries[self.general_entry_counter].grid(row=row_counter, column=2)

                self.general_entry_counter += 1
                row_counter += 1

        for key, value in self.data['General'].iteritems():
            if value['Field Type'] == 'Option':
                self.general_option_labels.append(Label(root, text=key))
                self.general_option_labels[self.general_option_counter].grid(sticky="W", row=row_counter, column=1)

                if isinstance(value['Selected'], bool):
                    value['Selected'] = str(value['Selected'])

                for index, item in enumerate(value['Values']):
                    if isinstance(item, bool):
                        value['Values'][index] = str(item)

                selected_field = StringVar(root)
                selected_field.set(value['Selected'])

                self.general_options.append(apply(OptionMenu, (root, selected_field) + tuple(value['Values'])))
                self.general_options[self.general_option_counter].grid(sticky="W", row=row_counter, column=2)

                self.general_option_counter += 1
                row_counter += 1
            elif value['Field Type'] == 'Interface':
                self.general_option_labels.append(Label(root, text=key))
                self.general_option_labels[self.general_option_counter].grid(sticky="W", row=row_counter, column=1)

                selected_field = StringVar(root)
                selected_field.set(value['Selected'])

                self.general_options.append(apply(OptionMenu, (root, selected_field) + tuple(netifaces.interfaces())))
                self.general_options[self.general_option_counter].grid(sticky="W", row=row_counter, column=2)

                self.general_option_counter += 1
                row_counter += 1

        self.archiving_entry_counter = 0
        self.archiving_option_counter = 0
        self.archiving_label_labels = []
        self.archiving_labels = []
        self.archiving_entry_labels = []
        self.archiving_entries = []
        self.archiving_option_labels = []
        self.archiving_options = []

        archiving_settings_label = Label(root, text="Archiving Settings")
        archiving_settings_label.grid(sticky="W", row=row_counter, column=2)
        row_counter += 1

        for key, value in self.data['Archiving'].iteritems():
            if value['Field Type'] == 'Entry':
                self.archiving_entry_labels.append(Label(root, text=key))
                self.archiving_entry_labels[self.archiving_entry_counter].grid(sticky="W", row=row_counter, column=1)

                self.archiving_entries.append(Entry(root))
                self.archiving_entries[self.archiving_entry_counter].insert(0, value['Value'])
                self.archiving_entries[self.archiving_entry_counter].grid(row=row_counter, column=2)

                self.archiving_entry_counter += 1
                row_counter += 1

        for key, value in self.data['Archiving'].iteritems():
            if value['Field Type'] == 'Option':
                self.archiving_option_labels.append(Label(root, text=key))
                self.archiving_option_labels[self.archiving_option_counter].grid(sticky="W", row=row_counter, column=1)

                if isinstance(value['Selected'], bool):
                    value['Selected'] = str(value['Selected'])

                for index, item in enumerate(value['Values']):
                    if isinstance(item, bool):
                        value['Values'][index] = str(item)

                selected_field = StringVar(root)
                selected_field.set(value['Selected'])

                self.archiving_options.append(apply(OptionMenu, (root, selected_field) + tuple(value['Values'])))
                self.archiving_options[self.archiving_option_counter].grid(sticky="W", row=row_counter, column=2)

                self.archiving_option_counter += 1
                row_counter += 1

        button_add = Button(root, text="Add Entry", command=self.add_entry)
        button_add.grid(sticky="W", row=0, column=3)

        button_add = Button(root, text="Add Dropdown List", command=self.add_options)
        button_add.grid(sticky="W", row=1, column=3)

        button_remove = Button(root, text="Remove Configuration", command=self.remove)
        button_remove.grid(sticky="W", row=2, column=3)

        button_save = Button(root, text="Save", command=self.save)
        button_save.grid(sticky="W", row=3, column=3)

        if self.plugin_name == 'netscanner':
            if len(self.data['Devices']['Banned Ids']) <= 1:
                for button in root.grid_slaves():
                    if int(button.grid_info()["row"]) == 5:
                        if int(button.grid_info()["column"]) == 3:
                            button.grid_forget()

            button_add_to_blacklist = Button(root, text="Add To Blacklist", command=self.add_to_blacklist)
            button_add_to_blacklist.grid(sticky="W", row=4, column=3)
            if len(self.data['Devices']['Banned Ids']) > 0:
                button_remove_from_blacklist = Button(root, text="Remove From Blacklist",
                                                      command=self.remove_from_blacklist)
                button_remove_from_blacklist.grid(sticky="W", row=5, column=3)
        else:
            for button in root.grid_slaves():
                if int(button.grid_info()["row"]) >= 4:
                    if int(button.grid_info()["column"]) == 3:
                        button.grid_forget()

    def add_entry(self):
        AddEntryView(self.root, self.base_dir, self.plugin_name, self.config_file_name)

    def add_options(self):
        AddOptionsView(self.root, self.base_dir, self.plugin_name, self.config_file_name)

    def remove(self):
        RemoveConfigurationView(self.root, self.base_dir, self.plugin_name, self.config_file_name)

    def add_to_blacklist(self):
        AddToBlacklistView(self.root, self.base_dir, self.plugin_name, self.config_file_name)

    def remove_from_blacklist(self):
        RemoveFromBlacklistView(self.root, self.base_dir, self.plugin_name, self.config_file_name)

    def save(self):
        if os.path.isfile(self.file_path):
            with open(self.file_path) as data_file:
                data = json.load(data_file)

                for item in range(self.general_entry_counter):
                    if not data['General'][self.general_entry_labels[item].cget("text")]["Is Path Type"]:
                        data['General'][self.general_entry_labels[item].cget("text")]["Value"] = self.general_entries[
                            item].get()
                    else:
                        data['General'][self.general_entry_labels[item].cget("text")]["Value"] = self.general_entries[
                            item].get()

                    with open(self.file_path, 'w') as outfile:
                        json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))

                for item in range(self.general_option_counter):
                    stored_value = self.general_options[item].cget("text")

                    if stored_value == 'True':
                        stored_value = True
                    elif stored_value == 'False':
                        stored_value = False

                    data['General'][self.general_option_labels[item].cget("text")]["Selected"] = stored_value

                    with open(self.file_path, 'w') as outfile:
                        json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))

                for item in range(self.archiving_entry_counter):
                    if not data['Archiving'][self.archiving_entry_labels[item].cget("text")]["Is Path Type"]:
                        data['Archiving'][self.archiving_entry_labels[item].cget("text")]["Value"] = \
                            self.archiving_entries[item].get()
                    else:
                        data['Archiving'][self.archiving_entry_labels[item].cget("text")]["Value"] = \
                            self.archiving_entries[item].get()

                    with open(self.file_path, 'w') as outfile:
                        json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))

                for item in range(self.archiving_option_counter):
                    stored_value = self.archiving_options[item].cget("text")

                    if stored_value == 'True':
                        stored_value = True
                    elif stored_value == 'False':
                        stored_value = False

                    data['Archiving'][self.archiving_option_labels[item].cget("text")]["Selected"] = stored_value

                    with open(self.file_path, 'w') as outfile:
                        json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))
