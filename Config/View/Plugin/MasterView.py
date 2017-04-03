import os.path
from Tkinter import *
from Config.View.Plugin import DynamicView
from Config.View.RemoveFields import RemoveFields


class MakePluginsView:
    def __init__(self, base_dir, config_file_name):
        self.plugin_names = [directory for directory in os.listdir(os.path.join(base_dir, 'plugins', 'collectors')) if
                             os.path.isdir(os.path.join(base_dir, 'plugins', 'collectors', directory))]

        root = Tk()

        label_plugins = Label(root, text="Plugins")

        selected_plugin = StringVar(root)
        selected_plugin.set(self.plugin_names[0])

        def select_plugin(val):
            RemoveFields(root)
            DynamicView.MakeView(root, base_dir, val, config_file_name)

        plugin_dropdown_list = OptionMenu(root, selected_plugin, *self.plugin_names, command=select_plugin)

        DynamicView.MakeView(root, base_dir, self.plugin_names[0], config_file_name)

        button_close = Button(root, text="Close", command=root.destroy)

        label_plugins.grid(sticky="W", row=0)
        plugin_dropdown_list.grid(sticky="W", row=1)
        button_close.grid(sticky="W", row=2)

        root.minsize(width=500, height=250)
        root.wm_title("Configure Plugin Settings")
        mainloop()
