import gtk
import os.path
import re
import sys
import netifaces
import traceback

import definitions

class PluginConfigGUI(gtk.Window):
    def __init__(self, parent, plugins):
        super(PluginConfigGUI, self).__init__()
        self.main_gui = parent

        self.value_type_create = {
            "text": self.create_text_hbox,
            "number": self.create_number_hbox,
            "checkbox": self.create_checkbox_hbox,
            "radio": self.create_radio_hbox,
            "option": self.create_option_hbox,
            "options": self.create_options_hbox,
            "netiface": self.create_netiface_hbox,
            "netifaces": self.create_netifaces_hbox,
            "filepath": self.create_filepath_hbox,
            "path": self.create_path_hbox
        }

        self.set_title("Plugin Configurations")
        self.set_modal(True)
        self.set_transient_for(self.main_gui)
        self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        #self.set_size_request(500, 700)
        self.set_border_width(6)
        self.set_resizable(False)

        self.plugins = plugins
        plugin_names = [plugin.name for plugin in self.plugins]

        vbox_main = gtk.VBox()

        hbox_plugins = gtk.HBox()
        frame_plugin_confs = gtk.Frame("Plugin Configurations:")

        self.vbox_plugin_main = None

        label_plugins = gtk.Label("Plugin")
        combobox_plugins = gtk.combo_box_new_text()
        for label in plugin_names:
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
        self.save_current_plugin_configs()

        self.show_plugin_configs(combobox.get_active_text(), frame)

    def show_plugin_configs(self, plugin, frame):
        if self.vbox_plugin_main:
            frame.remove(self.vbox_plugin_main)
        self.vbox_plugin_main = gtk.VBox()

        try:
            # self.current_plugin_config = plugin.PluginConfig(plugin)

            #TODO: remove try/catch stuff: Move to where it's created

            self.current_plugin = self.get_plugin_by_name(plugin)
            self.current_plugin_config = self.current_plugin.config
            if not self.current_plugin.is_running():
                self.current_plugin_config.refresh_data()
        except ValueError:
            traceback.print_exc()

            self.current_plugin_config = None
            self.vbox_plugin_main = self.create_error_vbox("Error loading the configuration files")
        else:
            self.plugin_config_widgets = []
            self.plugin_config_traces = []
            self.sensitivity_groups = []
            self.sensitivity_groups_switch = []

            self.vbox_plugin_main = self.create_config_vbox(
                self.current_plugin_config.get_configs_data(),
                self.current_plugin_config.get_schema_configs_data(),
                self.current_plugin_config.get_schema_configs_constraints(),
                "")

            for sensitivity_group, switch in zip(self.sensitivity_groups, self.sensitivity_groups_switch):
                self.enabled_checkbox_toggled(switch, sensitivity_group)

        if self.current_plugin.is_running():
            self.vbox_plugin_main.set_sensitive(False)

        frame.add(self.vbox_plugin_main)

        self.show_all()

    def create_config_vbox(self, inputs, types, constraints, trace_str):
        vbox_main = gtk.VBox()

        sensitivity_group = []

        for (key, value), (_, value_type) in zip(inputs.items(), types.items()):
            delimiter = self.current_plugin_config.TRACE_DELIMITER
            if trace_str == "":
                delimiter = ""
            cur_trace_str = trace_str + delimiter + str(key)
            if isinstance(value_type, dict):
                frame = gtk.Frame(key.title() + ":")
                sensitivity_group.append(frame)
                vbox_main.pack_start(frame)
                vbox_frame = self.create_config_vbox(inputs[key], value_type, constraints, cur_trace_str)
                frame.add(vbox_frame)
            else:
                if cur_trace_str in constraints:
                    constraint = constraints[cur_trace_str]
                    item = self.value_type_create.get(value_type, self.create_other_hbox)(
                        key, inputs[key], cur_trace_str, sensitivity_group, constraint)
                else:
                    item = self.value_type_create.get(value_type, self.create_other_hbox)(
                        key, inputs[key], cur_trace_str, sensitivity_group)
                vbox_main.pack_start(item)

        return vbox_main

    def create_error_vbox(self, error_msg):
        vbox_error = gtk.VBox()

        traceback.print_exc()
        err_label = gtk.Label(error_msg)
        err_label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("red"))
        vbox_error.pack_start(err_label)

        return vbox_error

    #TODO: Refactor these functions
    def create_text_hbox(self, label, value, trace, sensitivity_group, constraints=None):
        hbox_main = gtk.HBox()
        label_text = gtk.Label(label.title())
        label_text.set_alignment(0, 0.5)
        label_text.set_padding(8,8)
        entry_text = gtk.Entry()
        entry_text.set_text(value)
        hbox_main.pack_start(label_text)
        hbox_main.pack_start(entry_text)

        self.plugin_config_widgets.append(entry_text)
        self.plugin_config_traces.append(trace)
        sensitivity_group.append(label_text)
        sensitivity_group.append(entry_text)

        return hbox_main

    def create_number_hbox(self, label, value, trace, sensitivity_group, constraints=None):
        hbox_main = gtk.HBox()
        label_text = gtk.Label(label.title())
        label_text.set_alignment(0, 0.5)
        label_text.set_padding(8,8)
        adjustment = gtk.Adjustment(value, 0, sys.maxint, 1)
        spinbutton_value = gtk.SpinButton(adjustment)
        spinbutton_value.set_value(value)
        hbox_main.pack_start(label_text)
        hbox_main.pack_start(spinbutton_value)

        self.plugin_config_widgets.append(spinbutton_value)
        self.plugin_config_traces.append(trace)
        sensitivity_group.append(label_text)
        sensitivity_group.append(spinbutton_value)

        return hbox_main

    def create_checkbox_hbox(self, label, value, trace, sensitivity_group, constraints=None):
        hbox_main = gtk.HBox()
        checkbutton_option = gtk.CheckButton(label.title())
        checkbutton_option.set_active(value)
        if label.lower() == "enabled":
            checkbutton_option.connect("toggled", self.enabled_checkbox_toggled, sensitivity_group)
        hbox_main.pack_start(checkbutton_option)

        self.plugin_config_widgets.append(checkbutton_option)
        self.plugin_config_traces.append(trace)
        sensitivity_group.append(checkbutton_option)
        self.sensitivity_groups.append(sensitivity_group)
        self.sensitivity_groups_switch.append(checkbutton_option)

        return hbox_main

    def enabled_checkbox_toggled(self, widget, sensitivity_group):
        for item in sensitivity_group:
            if item is not widget:
                item.set_sensitive(widget.get_active())

    def create_radio_hbox(self, label, value, trace, sensitivity_group, constraints=None):
        hbox_main = gtk.HBox()
        label_text = gtk.Label(label.title())
        label_text.set_alignment(0, 0.5)
        label_text.set_padding(8,8)
        radiobuttons = []
        if constraints is None:
            options = [value]
        else:
            options = constraints
        previous_button = None
        for option in options:
            new_button = gtk.RadioButton(previous_button, option)
            if option == value:
                new_button.set_active(True)
            radiobuttons.append(new_button)
            previous_button = new_button
        hbox_main.pack_start(label_text)
        for radiobutton in radiobuttons:
            hbox_main.pack_start(radiobutton)

        self.plugin_config_widgets.append(radiobuttons)
        self.plugin_config_traces.append(trace)
        sensitivity_group.append(label_text)
        sensitivity_group.append(radiobuttons)

        return hbox_main

    def create_option_hbox(self, label, value, trace, sensitivity_group, constraints=None):
        hbox_main = gtk.HBox()
        label_options = gtk.Label(label.title())
        label_options.set_alignment(0, 0.5)
        label_options.set_padding(8,8)
        combobox_options = gtk.combo_box_new_text()
        if constraints is None:
            options = []
        else:
            options = constraints
        for option in options:
            combobox_options.append_text(option)
        selected_index = options.index(value)
        combobox_options.set_active(selected_index)
        hbox_main.pack_start(label_options)
        hbox_main.pack_start(combobox_options)

        self.plugin_config_widgets.append(combobox_options)
        self.plugin_config_traces.append(trace)
        sensitivity_group.append(label_options)
        sensitivity_group.append(combobox_options)

        return hbox_main

    def create_options_hbox(self, label, value, trace, sensitivity_group, constraints=None):
        hbox_main = gtk.HBox()
        label_text = gtk.Label(label.title())
        label_text.set_alignment(0, 0.5)
        label_text.set_padding(8,8)
        checkbuttons = []
        selected_options = value
        if constraints is None:
            options = []
        else:
            options = constraints
        for option in options:
            new_button = gtk.CheckButton(option)
            if option in selected_options:
                new_button.set_active(True)
            checkbuttons.append(new_button)
        hbox_main.pack_start(label_text)
        for checkbutton in checkbuttons:
            hbox_main.pack_start(checkbutton)

        self.plugin_config_widgets.append(checkbuttons)
        self.plugin_config_traces.append(trace)
        sensitivity_group.append(label_text)
        sensitivity_group.append(checkbuttons)

        return hbox_main

    def create_path_hbox(self, label, value, trace, sensitivity_group, constraints=None):
        hbox_main = gtk.HBox()
        label_text = gtk.Label(label.title())
        label_text.set_alignment(0, 0.5)
        label_text.set_padding(8,8)
        entry_filepath = gtk.Entry()
        entry_filepath.set_text(value)
        button_select_folder = gtk.ToolButton(
            gtk.image_new_from_file(os.path.join(os.path.join(os.getcwd(), "GUI"), "open_small.png")))
        button_select_folder.connect("clicked", self.select_folder, entry_filepath)
        hbox_main.pack_start(label_text)
        hbox_main.pack_start(entry_filepath)
        hbox_main.pack_start(button_select_folder)

        self.plugin_config_widgets.append(entry_filepath)
        self.plugin_config_traces.append(trace)
        sensitivity_group.append(label_text)
        sensitivity_group.append(entry_filepath)
        sensitivity_group.append(button_select_folder)

        return hbox_main

    def create_filepath_hbox(self, label, value, trace, sensitivity_group, constraints=None):
        hbox_main = gtk.HBox()
        label_text = gtk.Label(label.title())
        label_text.set_alignment(0, 0.5)
        label_text.set_padding(8,8)
        entry_filepath = gtk.Entry()
        entry_filepath.set_text(value)
        button_select_folder = gtk.ToolButton(
            gtk.image_new_from_file(os.path.join(os.path.join(os.getcwd(), "GUI"), "open_small.png")))
        button_select_folder.connect("clicked", self.select_file, entry_filepath)
        hbox_main.pack_start(label_text)
        hbox_main.pack_start(entry_filepath)
        hbox_main.pack_start(button_select_folder)

        self.plugin_config_widgets.append(entry_filepath)
        self.plugin_config_traces.append(trace)
        sensitivity_group.append(label_text)
        sensitivity_group.append(entry_filepath)
        sensitivity_group.append(button_select_folder)

        return hbox_main

    def create_netiface_hbox(self, label, value, trace, sensitivity_group, constraints=None):
        return self.create_option_hbox(
            label, value, trace, sensitivity_group, netifaces.interfaces())

    def create_netifaces_hbox(self, label, value, trace, sensitivity_group, constraints=None):
        return self.create_options_hbox(
            label, value, trace, sensitivity_group, netifaces.interfaces())

    def create_other_hbox(self, label, value, trace, constraints=None, sensitivity_group=None):
        return gtk.HBox()

    def select_file(self, event, entry_filepath):
        dialog_select_folder = gtk.FileChooserDialog()
        dialog_select_folder.set_title("Select File")
        dialog_select_folder.set_transient_for(self)
        dialog_select_folder.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)
        dialog_select_folder.set_filename(entry_filepath.get_text())

        response = dialog_select_folder.run()
        if response == gtk.RESPONSE_OK:
            entry_filepath.set_text(dialog_select_folder.get_filename())

        dialog_select_folder.destroy()

    def select_folder(self, event, entry_filepath):
        dialog_select_folder = gtk.FileChooserDialog()
        dialog_select_folder.set_title("Select Folder")
        dialog_select_folder.set_transient_for(self)
        dialog_select_folder.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        dialog_select_folder.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)
        dialog_select_folder.set_current_folder(entry_filepath.get_text())

        response = dialog_select_folder.run()
        if response == gtk.RESPONSE_OK:
            entry_filepath.set_text(dialog_select_folder.get_filename())

        dialog_select_folder.destroy()

    def save_current_plugin_configs(self):
        if not self.current_plugin_config:
            return

        for widget, trace in zip(self.plugin_config_widgets, self.plugin_config_traces):
            widget_type = self.current_plugin_config.get_schema_configs_data_field(trace)
            if widget_type == "text" or widget_type == "filepath" or widget_type == "path":
                value = "\"" + widget.get_text() + "\""
            elif widget_type == "number":
                value = int(widget.get_value())
            elif widget_type == "checkbox":
                value = widget.get_active()
            elif widget_type == "radio":
                for w in widget:
                    if w.get_active():
                        value = "\"" + w.get_label() + "\""
            elif widget_type == "option" or widget_type == "netiface":
                value = "\"" + widget.get_active_text() + "\""
            elif widget_type == "options" or widget_type == "netifaces":
                value = []
                for w in widget:
                    if w.get_active():
                        value.append(w.get_label())
            self.current_plugin_config.set_configs_data_field(trace, value)

        self.current_plugin_config.save_data()

    #TODO: Use this or engine's?
    def get_plugin_by_name(self, plugin_name):
        return next(plugin for plugin in self.plugins if plugin.name == plugin_name)


    #TODO: Remove when no longer necessary
    def close_plugin_config_dialog(self, event):
        self.save_current_plugin_configs()

        self.show_alert_message("Please restart ECEL for changes to take effect.")

        self.hide_all()

    #TODO: move these to basic lib
    def show_alert_message(self, msg):
        alert = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
                                      gtk.BUTTONS_CLOSE, msg)
        alert.run()
        alert.destroy()
