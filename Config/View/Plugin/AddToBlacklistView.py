import json
import os
import os.path
from Tkinter import *
import DynamicView
from Config.View.RemoveFields import RemoveFields


class AddToBlacklistView:
    def __init__(self, root, base_dir, plugin_name, config_file_name):
        self.root = root
        self.base_dir = base_dir
        self.config_file_name = config_file_name
        self.file_path = os.path.join(self.base_dir, 'plugins', 'collectors', plugin_name, config_file_name)

        self.plugin_name = plugin_name

        self.top = Toplevel()
        self.top.title("Add Interfaces To Blacklist")
        self.top.minsize(width=350, height=150)

        if os.path.isfile(self.file_path):
            with open(self.file_path) as data_file:
                self.data = json.load(data_file)

                self.ids = self.data['Devices']['Ids']
                self.interfaces = self.data['Devices']['Interfaces']
                self.banned = self.data['Devices']['Banned Interfaces']

                self.allowed = [x for x in self.interfaces if x not in self.banned]

        self.selected_config = StringVar(self.top)
        self.selected_config.set(self.allowed[0])

        plugin_dropdown_list = apply(OptionMenu, (self.top, self.selected_config) + tuple(self.allowed))
        plugin_dropdown_list.grid(sticky="W", row=0)

        button_add = Button(self.top, text="Add To Blacklist", command=self.add_to_blacklist)
        button_add.grid(sticky="W", row=1)

        button_close = Button(self.top, text="Close", command=self.top.destroy)
        button_close.grid(sticky="W", row=1, column=1)

    def add_to_blacklist(self):
        if os.path.isfile(self.file_path):
            with open(self.file_path) as data_file:
                data = json.load(data_file)

                data['Devices']['Banned Ids'].append(self.ids[self.interfaces.index(self.selected_config.get())])
                data['Devices']['Banned Interfaces'].append(self.selected_config.get())

                flag = data['General']['Flags']['Value']
                flag = flag.replace(self.ids[self.interfaces.index(self.selected_config.get())], "  ")
                flag = re.sub(' +', ' ', flag)
                data['General']['Flags']['Value'] = flag

                with open(self.file_path, 'w') as outfile:
                    json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))

        RemoveFields(self.root)
        DynamicView.MakeView(self.root, self.base_dir, self.plugin_name, self.config_file_name)

        self.top.destroy()
