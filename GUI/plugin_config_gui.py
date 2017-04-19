import gtk
import json
import os.path

class Plugin_Config_GUI(gtk.Window):
    def __init__(self, parent, base_dir, config_file_name):
        super(Plugin_Config_GUI, self).__init__()

        self.main_gui = parent
        self.base_dir = base_dir
        self.config_file_name = config_file_name

        self.set_title("Plugin Configurations")
        self.set_modal(True)
        self.set_transient_for(self.main_gui)
        self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        # self.set_size_request(500, 250)
        # self.set_resizable(False)

        self.plugin_names = [directory for directory in os.listdir(os.path.join(base_dir, 'plugins', 'collectors')) if
                             os.path.isdir(os.path.join(base_dir, 'plugins', 'collectors', directory))]

        vbox_main = gtk.VBox()
        hbox_plugins = gtk.HBox()
        frame_plugin_confs = gtk.Frame("Plugin Configurations:")

        self.vbox_main = None

        label_plugins = gtk.Label("Plugins")
        combobox_plugins = gtk.combo_box_new_text()
        for label in self.plugin_names:
            combobox_plugins.append_text(label)
        combobox_plugins.set_active(0)
        combobox_plugins.connect('changed', self.select_plugin, combobox_plugins, frame_plugin_confs)

        button_close = gtk.Button("Close")
        button_close.connect("clicked", self.close_plugin_config_dialog)

        hbox_plugins.pack_start(label_plugins)
        hbox_plugins.pack_start(combobox_plugins)
        vbox_main.pack_start(hbox_plugins)
        vbox_main.pack_start(frame_plugin_confs)
        vbox_main.pack_start(button_close)

        self.show_plugin_configs(combobox_plugins.get_active_text(), frame_plugin_confs)

        self.add(vbox_main)
        self.show_all()

    def select_plugin(self, event, combobox, frame):
        self.save_plugin_configs()

        self.show_plugin_configs(combobox.get_active_text(), frame)

    def show_plugin_configs(self, plugin_name, frame):
        self.file_path = os.path.join(self.base_dir, 'plugins', 'collectors', plugin_name, self.config_file_name)

        if self.vbox_main:
            frame.remove(self.vbox_main)
        self.vbox_main = gtk.VBox()

        type_counter = 0
        self.types = []
        self.entry_counter = []
        self.option_counter = []
        self.entry_labels = []
        self.entries = []
        self.option_labels = []
        self.options = []

        if os.path.isfile(self.file_path):
            with open(self.file_path) as data_file:
                self.data = json.load(data_file)

        for setting_type, settings in self.data.iteritems():
            self.entry_labels.append([])
            self.entries.append([])
            self.option_labels.append([])
            self.options.append([])
            self.entry_counter.append(0)
            self.option_counter.append(0)

            vbox = gtk.VBox()

            self.types.append(setting_type)

            settings_label = gtk.Frame(setting_type + " Settings:")
            self.vbox_main.pack_start(settings_label)

            for key, value in self.data[setting_type].iteritems():
                hbox = gtk.HBox()

                if value['Field Type'] == 'Entry':
                    self.entry_labels[type_counter].append(gtk.Label(key))
                    hbox.pack_start(self.entry_labels[type_counter][self.entry_counter[type_counter]])

                    self.entries[type_counter].append(gtk.Entry())
                    self.entries[type_counter][self.entry_counter[type_counter]].set_text(value['Value'])

                    hbox.pack_start(self.entries[type_counter][self.entry_counter[type_counter]])

                    self.entry_counter[type_counter] += 1

                if value['Field Type'] == 'Option':
                    self.option_labels[type_counter].append(gtk.Label(key))
                    hbox.pack_start(self.option_labels[type_counter][self.option_counter[type_counter]])

                    if isinstance(value['Selected'], bool):
                        value['Selected'] = str(value['Selected'])

                    for index, item in enumerate(value['Values']):
                        if isinstance(item, bool):
                            value['Values'][index] = str(item)

                    selected_index = value['Values'].index(value['Selected'])

                    combobox = gtk.combo_box_new_text()
                    for vals in value['Values']:
                        combobox.append_text(vals)
                    combobox.set_active(selected_index)

                    self.options[type_counter].append(combobox)

                    hbox.pack_start(self.options[type_counter][self.option_counter[type_counter]])

                    self.option_counter[type_counter] += 1

                vbox.add(hbox)

            settings_label.add(vbox)
            type_counter += 1

        frame.add(self.vbox_main)

        self.show_all()

    def save_plugin_configs(self):
        if os.path.isfile(self.file_path):
            with open(self.file_path) as data_file:
                data = json.load(data_file)

                for type_counter, type in enumerate(self.types):
                    for item in range(self.entry_counter[type_counter]):
                        data[type][self.entry_labels[type_counter][item].get_text()]["Value"] = self.entries[type_counter][item].get_text()

                        with open(self.file_path, 'w') as outfile:
                            json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))

                    for item in range(self.option_counter[type_counter]):
                        stored_value = self.options[type_counter][item].get_active_text()

                        if stored_value == 'True':
                            stored_value = True
                        elif stored_value == 'False':
                            stored_value = False

                        data[type][self.option_labels[type_counter][item].get_text()]["Selected"] = stored_value

                        with open(self.file_path, 'w') as outfile:
                            json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))

    def close_plugin_config_dialog(self, event):
        self.save_plugin_configs()

        self.show_alert_message("Please restart ECEL for changes to take effect.")

        self.hide_all()

    def show_alert_message(self, msg):
        alert = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
                                      gtk.BUTTONS_CLOSE, msg)
        alert.run()
        alert.destroy()
