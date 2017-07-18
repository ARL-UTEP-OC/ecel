import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk
import os.path
import sys
import netifaces
import traceback
import definitions

class PluginConfigGUI(Gtk.Frame):
    def __init__(self, parent, collector):
        super(PluginConfigGUI, self).__init__()
        self.main_gui = parent

        #TODO: Add one for compression format
        self.value_type_create = {
            "text": self.create_text_hbox,
            "number": self.create_number_hbox,
            "checkbox": self.create_checkbox_hbox,
            "radio": self.create_radio_hbox,
            "option": self.create_option_hbox,
            "options": self.create_options_hbox,
            "time": self.create_time_hbox,
            "netiface": self.create_netiface_hbox,
            "netifaces": self.create_netifaces_hbox,
            "filepath": self.create_filepath_hbox,
            "path": self.create_path_hbox
        }

        self.vbox_main = Gtk.VBox()

        headerBox = Gtk.Box()
        headerLabel = Gtk.Label()
        headerLabel.set_label(collector.name + " Plugin Configurations")
        headerBox.add(headerLabel)
        headerBox.get_style_context().add_class("config-header")
        headerLabel.set_margin_left(definitions.CONFIG_WINDOW_WIDTH / 3) # center align text in header box

        frame_plugin_confs = Gtk.Frame()
        frame_plugin_confs.set_name("Plugin Configurations:");

        self.vbox_plugin_main = None

        self.button_save= Gtk.Button("Save")
        self.button_save.connect("clicked", self.close_plugin_config_dialog)

        self.vbox_main.pack_start(headerBox, True, True, 0)
        self.vbox_main.pack_start(frame_plugin_confs, True, True, 0)
        self.vbox_main.pack_start(self.button_save, True, True, 0)

        self.show_plugin_configs(collector, frame_plugin_confs)

        self.add(self.vbox_main)

        self.vbox_plugin_main.set_sensitive(True)
        self.vbox_main.set_sensitive(True)
        headerBox.set_sensitive(True)
        frame_plugin_confs.set_sensitive(True)
        self.set_sensitive(True)
        self.button_save.set_sensitive(False)

    def enable_save_button(self,widget,event):
        self.button_save.set_sensitive(True)

    def get_plugin_frame(self):
        return self.vbox_main

    def select_plugin(self, event, combobox, frame):
        self.save_current_plugin_configs()
        self.show_plugin_configs(combobox.get_active_text(), frame)

    def show_plugin_configs(self, collector, frame):
        if self.vbox_plugin_main:
            frame.remove(self.vbox_plugin_main)
        self.vbox_plugin_main = Gtk.VBox()

        self.current_plugin = collector
        self.current_plugin_config = self.current_plugin.config
        if not self.current_plugin.is_running():
            self.current_plugin_config.refresh_data()

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
        vbox_main = Gtk.VBox()

        sensitivity_group = []

        for (key, value), (_, value_type) in zip(inputs.items(), types.items()):
            delimiter = self.current_plugin_config.TRACE_DELIMITER
            if trace_str == "":
                delimiter = ""
            cur_trace_str = trace_str + delimiter + str(key)
            if isinstance(value_type, dict):
                frame = Gtk.Frame()
                frame.set_label(key.title() + ":")
                sensitivity_group.append(frame)
                vbox_main.pack_start(frame, True, True, 0)
                vbox_frame = self.create_config_vbox(inputs[key], value_type, constraints, cur_trace_str)
                frame.add(vbox_frame)
            else:
                if cur_trace_str in constraints:
                    constraint = constraints[cur_trace_str]
                    item = self.value_type_create.get(value_type, self.create_error_hbox)(
                        key, inputs[key], cur_trace_str, sensitivity_group, constraint)
                else:
                    item = self.value_type_create.get(value_type, self.create_error_hbox)(
                        key, inputs[key], cur_trace_str, sensitivity_group)
                vbox_main.pack_start(item, True, True, 0)

        return vbox_main

    def create_error_vbox(self, error_msg):
        vbox_error = Gtk.VBox()

        traceback.print_exc()
        err_label = Gtk.Label(label=error_msg)
        err_label.modify_fg(Gtk.StateType.NORMAL, Gdk.color_parse("red"))
        vbox_error.pack_start(err_label, True, True, 0)

        return vbox_error

    def create_error_hbox(self, label, value, trace, constraints=None, sensitivity_group=None):
        return self.create_error_vbox("ERROR: Invalid type")

    #TODO: Refactor these functions
    def create_text_hbox(self, label, value, trace, sensitivity_group, constraints=None):
        hbox_main = Gtk.HBox()
        label_text = Gtk.Label(label=label.title())
        label_text.set_alignment(0, 0.5)
        label_text.set_padding(8,8)
        entry_text = Gtk.Entry()
        entry_text.connect("button-press-event",self.enable_save_button)
        entry_text.set_text(value)
        hbox_main.pack_start(label_text, True, True, 0)
        hbox_main.pack_start(entry_text, True, True, 0)

        self.plugin_config_widgets.append(entry_text)
        self.plugin_config_traces.append(trace)
        sensitivity_group.append(label_text)
        sensitivity_group.append(entry_text)

        return hbox_main

    def create_number_hbox(self, label, value, trace, sensitivity_group, constraints=None):
        hbox_main = Gtk.HBox()
        label_text = Gtk.Label(label=label.title())
        adjustment = Gtk.Adjustment(value, 0, sys.maxint, 1)
        spinbutton_value = Gtk.SpinButton(adjustment)
        spinbutton_value.connect("event",self.enable_save_button,None)
        spinbutton_value.set_value(value)
        hbox_main.pack_start(label_text, True, True, 0)
        hbox_main.pack_start(spinbutton_value, True, True, 0)

        self.plugin_config_widgets.append(spinbutton_value)
        self.plugin_config_traces.append(trace)
        sensitivity_group.append(label_text)
        sensitivity_group.append(spinbutton_value)

        return hbox_main

    def create_checkbox_hbox(self, label, value, trace, sensitivity_group, constraints=None):
        hbox_main = Gtk.HBox()
        checkbutton_option = Gtk.CheckButton(label.title())
        checkbutton_option.set_active(value)
        if label.lower() == "enabled":
            checkbutton_option.connect("toggled", self.enabled_checkbox_toggled, sensitivity_group)
        hbox_main.pack_start(checkbutton_option, True, True, 0)

        self.plugin_config_widgets.append(checkbutton_option)
        self.plugin_config_traces.append(trace)
        sensitivity_group.append(checkbutton_option)
        self.sensitivity_groups.append(sensitivity_group)
        self.sensitivity_groups_switch.append(checkbutton_option)

        return hbox_main

    def enabled_checkbox_toggled(self, widget, sensitivity_group):
        self.enable_save_button(None,None)
        for item in sensitivity_group:
            if item is not widget:
                item.set_sensitive(widget.get_active())

    def create_radio_hbox(self, label, value, trace, sensitivity_group, constraints=None):
        hbox_main = Gtk.HBox()
        label_text = Gtk.Label(label=label.title())
        label_text.set_alignment(0, 0.5)
        label_text.set_padding(8,8)
        radiobuttons = []
        previous_button = None
        if constraints is None:
            options = [value]
        else:
            options = constraints
        for option in options:
            new_button = Gtk.RadioButton()
            new_button.set_label(option)
            if(previous_button != None):
                new_button = new_button.new_with_label_from_widget(previous_button,option)
            if option == value:
                new_button.set_active(True)
            radiobuttons.append(new_button)
            previous_button = new_button
        hbox_main.pack_start(label_text, True, True, 0)
        for radiobutton in radiobuttons:
            hbox_main.pack_start(radiobutton, True, True, 0)

        previous_button.connect("toggled",self.enable_save_button,None)
        self.plugin_config_widgets.append(radiobuttons)
        self.plugin_config_traces.append(trace)
        sensitivity_group.append(label_text)
        sensitivity_group.append(radiobuttons)

        return hbox_main

    def create_option_hbox(self, label, value, trace, sensitivity_group, constraints=None):
        hbox_main = Gtk.HBox()
        label_options = Gtk.Label(label=label.title())
        label_options.set_alignment(0, 0.5)
        label_options.set_padding(8,8)
        combobox_options = Gtk.ComboBoxText()
        combobox_options.connect("changed",self.enable_save_button,None)
        if constraints is None:
            options = []
        else:
            options = constraints
        for option in options:
            combobox_options.append_text(option)
        selected_index = options.index(value)
        combobox_options.set_active(selected_index)
        hbox_main.pack_start(label_options, True, True, 0)
        hbox_main.pack_start(combobox_options, True, True, 0)

        self.plugin_config_widgets.append(combobox_options)
        self.plugin_config_traces.append(trace)
        sensitivity_group.append(label_options)
        sensitivity_group.append(combobox_options)

        return hbox_main

    def create_options_hbox(self, label, value, trace, sensitivity_group, constraints=None):
        hbox_main = Gtk.HBox()
        label_text = Gtk.Label(label=label.title())
        label_text.set_alignment(0, 0.5)
        label_text.set_padding(8,8)
        checkbuttons = []
        selected_options = value
        if constraints is None:
            options = []
        else:
            options = constraints
        for option in options:
            new_button = Gtk.CheckButton(option)
            if option in selected_options:
                new_button.set_active(True)
            checkbuttons.append(new_button)
        hbox_main.pack_start(label_text, True, True, 0)
        for checkbutton in checkbuttons:
            hbox_main.pack_start(checkbutton, True, True, 0)

        self.plugin_config_widgets.append(checkbuttons)
        self.plugin_config_traces.append(trace)
        sensitivity_group.append(label_text)
        sensitivity_group.append(checkbuttons)

        return hbox_main

    def create_path_hbox(self, label, value, trace, sensitivity_group, constraints=None):
        hbox_main = Gtk.HBox()
        label_text = Gtk.Label(label=label.title())
        label_text.set_alignment(0, 0.5)
        label_text.set_padding(8,8)
        entry_filepath = Gtk.Entry()
        entry_filepath.set_text(value)
        image = Gtk.Image()
        image.set_from_file(os.path.join(definitions.ICONS_DIR, "open_small.png"))
        image.show()
        button_select_folder = Gtk.ToolButton()
        button_select_folder.set_icon_widget(image)
        button_select_folder.connect("clicked", self.select_folder, entry_filepath)
        hbox_main.pack_start(label_text, True, True, 0)
        hbox_main.pack_start(entry_filepath, True, True, 0)
        hbox_main.pack_start(button_select_folder, True, True, 0)

        self.plugin_config_widgets.append(entry_filepath)
        self.plugin_config_traces.append(trace)
        sensitivity_group.append(label_text)
        sensitivity_group.append(entry_filepath)
        sensitivity_group.append(button_select_folder)

        return hbox_main

    def create_filepath_hbox(self, label, value, trace, sensitivity_group, constraints=None):
        hbox_main = Gtk.HBox()
        label_text = Gtk.Label(label=label.title())
        label_text.set_alignment(0, 0.5)
        label_text.set_padding(8,8)
        entry_filepath = Gtk.Entry()
        entry_filepath.set_text(value)
        image = Gtk.Image()
        image.set_from_file(os.path.join(definitions.ICONS_DIR, "open_small.png"))
        image.show()
        button_select_folder = Gtk.ToolButton()
        button_select_folder.set_icon_widget(image)
        button_select_folder.connect("clicked", self.select_file, entry_filepath)
        hbox_main.pack_start(label_text, True, True, 0)
        hbox_main.pack_start(entry_filepath, True, True, 0)
        hbox_main.pack_start(button_select_folder, True, True, 0)

        self.plugin_config_widgets.append(entry_filepath)
        self.plugin_config_traces.append(trace)
        sensitivity_group.append(label_text)
        sensitivity_group.append(entry_filepath)
        sensitivity_group.append(button_select_folder)

        return hbox_main

    def create_time_hbox(self, label, value, trace, sensitivity_group, constraints=None):
        hbox_main = Gtk.HBox()
        label_text = Gtk.Label(label=label.title())
        label_text.set_alignment(0, 0.5)
        label_text.set_padding(8,8)
        adjustment = Gtk.Adjustment(value, 0, sys.maxint, 1)
        spinbutton_value = Gtk.SpinButton()
        spinbutton_value.set_adjustment(adjustment)
        spinbutton_value.connect("value-changed",self.enable_save_button, None)
        combobox_units = Gtk.ComboBoxText()
        combobox_units.connect("changed",self.enable_save_button,None)
        t_value, units = self.get_time_value_and_units(value)
        spinbutton_value.set_value(t_value)
        options = ["seconds", "minutes", "hours", "days", "weeks"]
        for option in options:
            combobox_units.append_text(option)
        selected_index = options.index(units)
        combobox_units.set_active(selected_index)
        hbox_main.pack_start(label_text, True, True, 0)
        hbox_main.pack_start(spinbutton_value, True, True, 0)
        hbox_main.pack_start(combobox_units, True, True, 0)

        self.plugin_config_widgets.append([spinbutton_value, combobox_units])
        self.plugin_config_traces.append(trace)
        sensitivity_group.append(label_text)
        sensitivity_group.append(spinbutton_value)

        return hbox_main

    #TODO: Refactor these
    def get_time_value_and_units(self, time):
        min_unit = 60
        hr_unit = min_unit * 60
        day_unit = hr_unit * 24
        week_unit = day_unit * 7

        unit = "seconds"

        if time % week_unit == 0:
            time = time / week_unit
            unit = "weeks"
        elif time % day_unit == 0:
            time = time / day_unit
            unit = "days"
        elif time % hr_unit == 0:
            time = time / hr_unit
            unit = "hours"
        elif time % min_unit == 0:
            time = time / min_unit
            unit = "minutes"

        return time, unit

    def get_time_from_value_and_units(self, time, units):
        min_unit = 60
        hr_unit = min_unit * 60
        day_unit = hr_unit * 24
        week_unit = day_unit * 7

        if units == "weeks":
            return time * week_unit
        if units == "days":
            return time * day_unit
        if units == "hours":
            return time * hr_unit
        if units == "minutes":
            return time * min_unit

        return time

    def create_netiface_hbox(self, label, value, trace, sensitivity_group, constraints=None):
        return self.create_option_hbox(
            label, value, trace, sensitivity_group, netifaces.interfaces())

    def create_netifaces_hbox(self, label, value, trace, sensitivity_group, constraints=None):
        return self.create_options_hbox(
            label, value, trace, sensitivity_group, netifaces.interfaces())

    def select_file(self, event, entry_filepath):
        dialog_select_folder = Gtk.FileChooserDialog()
        dialog_select_folder.set_title("Select File")
        dialog_select_folder.set_transient_for(self)
        dialog_select_folder.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        dialog_select_folder.set_filename(entry_filepath.get_text())

        response = dialog_select_folder.run()
        if response == Gtk.ResponseType.OK:
            entry_filepath.set_text(dialog_select_folder.get_filename())

        dialog_select_folder.destroy()

    def select_folder(self, event, entry_filepath):
        dialog_select_folder = Gtk.FileChooserDialog()
        dialog_select_folder.set_title("Select Folder")
        dialog_select_folder.set_transient_for(self)
        dialog_select_folder.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        dialog_select_folder.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        dialog_select_folder.set_current_folder(entry_filepath.get_text())

        response = dialog_select_folder.run()
        if response == Gtk.ResponseType.OK:
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
            elif widget_type == "time":
                value = self.get_time_from_value_and_units(int(widget[0].get_value()), widget[1].get_active_text())
            else:
                raise TypeError("Invalid widget type")
            self.current_plugin_config.set_configs_data_field(trace, value)

        self.current_plugin_config.save_data()

    def close_plugin_config_dialog(self, event):
        self.save_current_plugin_configs()
        self.current_plugin.refresh_data()
        self.hide()
        self.button_save.set_sensitive(False)
