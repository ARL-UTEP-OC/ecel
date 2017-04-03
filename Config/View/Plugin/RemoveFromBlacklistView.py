import json
import os
import os.path
from Tkinter import *
import DynamicView
from Config.View.RemoveFields import RemoveFields


class RemoveFromBlacklistView:
    def __init__(self, root, base_dir, plugin_name, config_file_name):
        self.root = root
        self.base_dir = base_dir
        self.config_file_name = config_file_name
        self.file_path = os.path.join(self.base_dir, 'plugins', 'collectors', plugin_name, config_file_name)

        self.plugin_name = plugin_name

        self.top = Toplevel()
        self.top.title("Remove Interfaces From Blacklist")
        self.top.minsize(width=350, height=150)

        if os.path.isfile(self.file_path):
            with open(self.file_path) as data_file:
                self.data = json.load(data_file)

                self.ids = self.data['Devices']['Ids']
                self.interfaces = self.data['Devices']['Interfaces']
                self.banned = self.data['Devices']['Banned Interfaces']
                self.banned_ids = self.data['Devices']['Banned Ids']

        self.selected_config = StringVar(self.top)
        self.selected_config.set(self.banned[0])

        plugin_dropdown_list = apply(OptionMenu, (self.top, self.selected_config) + tuple(self.banned))
        plugin_dropdown_list.grid(sticky="W", row=0)

        button_add = Button(self.top, text="Remove From Blacklist", command=self.remove_from_blacklist)
        button_add.grid(sticky="W", row=1)

        button_close = Button(self.top, text="Close", command=self.top.destroy)
        button_close.grid(sticky="W", row=1, column=1)

    def remove_from_blacklist(self):
        if os.path.isfile(self.file_path):
            with open(self.file_path) as data_file:
                data = json.load(data_file)

                data['Devices']['Banned Interfaces'].remove(self.selected_config.get())
                interfaces_id = int(self.interfaces.index(self.selected_config.get()))
                interfaces_id = (interfaces_id + 1)
                interfaces_id = str(interfaces_id)
                data['Devices']['Banned Ids'].remove(interfaces_id)

                self.banned_ids = data['Devices']['Banned Ids']

                with open(self.file_path, 'w') as outfile:
                    json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))

                self.update_flag()

        RemoveFields(self.root)
        DynamicView.MakeView(self.root, self.base_dir, self.plugin_name, self.config_file_name)

        self.top.destroy()

    def update_flag(self):
        if os.path.isfile(self.file_path):
            with open(self.file_path) as data_file:
                data = json.load(data_file)

                flag = [x for x in self.ids if x not in self.banned_ids]

                data['General']['Flags']['Value'] = "-i " + ' '.join(flag) + " -w"

                with open(self.file_path, 'w') as outfile:
                    json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))
