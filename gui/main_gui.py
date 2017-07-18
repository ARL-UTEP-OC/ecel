import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk
from utils.collector_action import Action
import os
import subprocess
import status_icon
import definitions
import engine.collector
from utils.css_provider import CssProvider
from gui.export_gui import ExportGUI
from gui.progress_bar import ProgressBar
from gui.plugin_config_gui import PluginConfigGUI
from _version import __version__

class MainGUI(Gtk.Window):

    def __init__(self, app_engine):
        super(MainGUI, self).__init__()

        self.set_title("Evaluator-Centric and Extensible Logger v%s" % (__version__))
        self.set_size_request(definitions.MAIN_WINDOW_WIDTH, definitions.MAIN_WINDOW_HEIGHT)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", self.hide_on_delete)

        self.engine = app_engine
        self.numCollectors = self.engine.get_collector_length()

        # Main container grid
        self.grid = Gtk.Grid()

        # Adds css file to be used in this window along with all of its children.
        # To add a css class to a widget: {widget}.get_style_context().add_class("css_class_name")
        self.cssProvider = CssProvider("widget_styles.css")

        self.startall_button = Gtk.ToolButton()
        self.startall_button.set_icon_widget(self.get_image("start.png"))
        self.startall_button.connect("clicked", self.process_active_collectors,Action.RUN)
        self.startall_button.set_sensitive(False)

        self.stopall_button = Gtk.ToolButton()
        self.stopall_button.set_icon_widget(self.get_image("stop.png"))
        self.stopall_button.connect("clicked", self.process_active_collectors,Action.STOP)
        self.stopall_button.set_sensitive(False)

        self.parseall_button = Gtk.ToolButton()
        self.parseall_button.set_icon_widget(self.get_image("json.png"))
        self.parseall_button.connect("clicked", self.process_active_collectors, Action.PARSE)

        self.export_button = Gtk.ToolButton()
        self.export_button.set_icon_widget(self.get_image("export.png"))
        self.export_button.connect("clicked", self.export_all)

        self.remove_data_button = Gtk.ToolButton()
        self.remove_data_button.set_icon_widget(self.get_image("delete.png"))
        self.remove_data_button.connect("clicked", self.delete_all)

        self.collector_config_button = Gtk.ToolButton()
        self.collector_config_button.set_icon_widget(self.get_image("settings.png"))
        self.collector_config_button.connect("clicked", self.configure_collectors)

        self.toolbarWidget = Gtk.Box()
        self.toolbarWidget.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.toolbarWidget.set_size_request(definitions.MAIN_WINDOW_WIDTH,definitions.TOOL_BAR_HEIGHT)
        self.toolbarWidget.add(self.create_toolbar())

        # List of Gtk.ListBoxRows representing collector plugins
        self.collectorList = Gtk.ListBox()
        self.collectorList.set_selection_mode(Gtk.SelectionMode.SINGLE)
        # Highlight/gray out list box rows depending on which collectors are marked active
        self.collectorList.connect("row-activated",self.update_row_colors)
        # Enable multiple collector selection when (SHIFT + CTRL) occurs (selection mode == MULTIPLE)
        self.collectorList.connect("key-press-event",self.ctrl_shift_enable_multiple_collector_selection)
        # Makes the next click revert back to single selection mode when (SHIFT + CTRL) released
        self.collectorList.connect("key-release-event",self.ctrl_shift_disable_multiple_collector_selection)

        # Container for the list of collector plugins
        self.collectorWidget = Gtk.Box()
        self.collectorWidget.set_orientation(Gtk.Orientation.VERTICAL)
        self.collectorWidget.set_size_request(definitions.COLLECTOR_WIDGET_WIDTH,definitions.MAIN_WINDOW_HEIGHT - definitions.TOOL_BAR_HEIGHT)
        self.collectorWidget.add(self.collectorList)

        self.currentConfigWindow = None

        # Area of grid where configuration window appears.
        self.configWidget = Gtk.Box()
        self.configWidget.set_size_request(definitions.CONFIG_WINDOW_WIDTH,definitions.CONFIG_WINDOW_HEIGHT)

        # contains collector widget AND config Widget
        self.main_body = Gtk.Box()
        self.main_body.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.main_body.add(self.collectorWidget)
        self.main_body.add(self.configWidget)

        self.grid.set_orientation(Gtk.Orientation.VERTICAL)
        self.grid.add(self.toolbarWidget)
        self.grid.add(self.main_body)

        self.add(self.grid)

        self.connect("destroy", self.close_all)

        for i, collector in enumerate(self.engine.collectors):
            print "%d) %s" % (i, collector.name)
            self.collectorList.add(self.create_collector_row(collector))

        self.show_all()
        self.status_context_menu = status_icon.CustomSystemTrayIcon(app_engine, self)

    # When (SHIFT + CTRL) occurs, enable multiple collector selection
    def ctrl_shift_enable_multiple_collector_selection(self, listBox, event):
        modifiers = Gtk.accelerator_get_default_mod_mask()
        if(((event.state & modifiers) == Gdk.ModifierType.CONTROL_MASK)
            | (event.state & modifiers) == Gdk.ModifierType.SHIFT_MASK
           ):
                self.collectorList.set_selection_mode(Gtk.SelectionMode.MULTIPLE)

    # When (SHIFT + CTRL) keys are released, revert back to single selection on next click
    def ctrl_shift_disable_multiple_collector_selection(self, listBox, event):
        modifiers = Gtk.accelerator_get_default_mod_mask()
        if (((event.state & modifiers) == Gdk.ModifierType.CONTROL_MASK) == False
                | ((event.state & modifiers) == Gdk.ModifierType.SHIFT_MASK) == False):
            # Next click will reset collector list to single selection mode
            # Next click because if we just reset to single selection now...
            # ...any selected collectors would be unselected automatically
            self.collectorList.connect("button-press-event",self.enable_single_selection)

    # Revert back to single selection only for collectors
    def enable_single_selection(self,lBox,event):
        # Left click
        if(event.button == Gdk.BUTTON_PRIMARY):
            # Unselect all rows
            self.collectorList.unselect_all()
            # Reset selection mode to single
            self.collectorList.set_selection_mode(Gtk.SelectionMode.SINGLE)
            # Disable this handler so that multiple selection is possible again in the future.
            self.collectorList.disconnect_by_func(self.enable_single_selection)

    def create_toolbar(self):
        toolbar = Gtk.Toolbar()
        toolbar.set_style(Gtk.ToolbarStyle.ICONS)
        toolbar.set_size_request(definitions.MAIN_WINDOW_WIDTH,definitions.TOOL_BAR_HEIGHT)

        separator1 = Gtk.SeparatorToolItem()
        separator2 = Gtk.SeparatorToolItem()
        separator3 = Gtk.SeparatorToolItem()

        self.startall_button.set_tooltip_text("Start All Selected Collectors")
        toolbar.insert(self.startall_button, 0)
        self.stopall_button.set_tooltip_text("Stop All Selected collectors")
        toolbar.insert(self.stopall_button, 1)
        toolbar.insert(separator1, 2)
        self.parseall_button.set_tooltip_text("Execute Selected Parsers")
        toolbar.insert(self.parseall_button, 3)
        toolbar.insert(separator2, 4)
        self.export_button.set_tooltip_text("Export All Collector Data")
        toolbar.insert(self.export_button, 5)
        self.remove_data_button.set_tooltip_text("Delete All Collector Data")
        toolbar.insert(self.remove_data_button, 6)

        return toolbar

    # Return image based on image name
    def get_image(self,name):
        image = Gtk.Image()
        image.set_from_file(os.path.join(definitions.ICONS_DIR, name))
        image.show()
        return image

    # Destroy anything in the current config window before placing new config window
    def clear_config_window(self):
        self.configWidget.foreach(self.delete_widget)

    # Helper for clear_config_window()
    def delete_widget(self,widget):
        widget.destroy()

    # Pull the collectors configuration from plugin_configure_gui.py and place in config window.
    def create_config_window(self,event,collector):
        self.clear_config_window()
        self.currentConfigWindow = PluginConfigGUI(self, collector).get_plugin_frame()
        self.currentConfigWindow.set_name(collector.name)
        self.currentConfigWindow.unparent()
        self.currentConfigWindow.show_all()
        self.currentConfigWindow.set_size_request(definitions.CONFIG_WINDOW_WIDTH,definitions.CONFIG_WINDOW_HEIGHT)
        self.currentConfigWindow.set_sensitive(not collector.is_running())
        self.configWidget.add(self.currentConfigWindow)
        self.configWidget.set_sensitive(True)

    def configure_collectors(self, event):
        PluginConfigGUI(self, self.engine.collectors)

    def show_gui(self):
        self.present()
        self.show_all()

    def export_all(self, event):
        ExportGUI(self)

    def delete_all(self, event):
        if self.show_confirmation_dialog("Are you sure you want to delete all collector data (this cannot be undone)?"):
            remove_cmd = os.path.join(os.path.join(os.getcwd(), "scripts"), "cleanCollectorData.sh")
            subprocess.call(remove_cmd) #TODO: Change this to not call external script

    # Create list box row for specific collector (left pane)
    def create_collector_row(self,collector):

        label = Gtk.Label()
        label.set_label(collector.name)

        row = Gtk.ListBoxRow()
        row_height = definitions.MAIN_WINDOW_HEIGHT / self.numCollectors
        row.set_size_request(definitions.COLLECTOR_WIDGET_WIDTH,row_height)
        row.set_name(collector.name)

        box = Gtk.EventBox()
        box.add(label)
        box.connect("button-press-event",self.collector_listbox_handler,collector.name)

        row.add(box)
        row.get_style_context().add_class("listBoxRow")
        row.get_style_context().add_class("inactive-color")

        return row

    # Show options over collector row on right click
    def collector_listbox_handler(self, eventBox, event, collectorName):

        collector = self.engine.get_collector(collectorName)

        # Left click AND selection mode == SINGLE
        if(event.button == Gdk.BUTTON_PRIMARY and (self.collectorList.get_selection_mode() == Gtk.SelectionMode.SINGLE)):
            self.create_config_window(event,collector)

        if(event.button == Gdk.BUTTON_SECONDARY): # right click
            menu = Gtk.Menu()

            runItem = Gtk.MenuItem("Run " + collector.name)
            runItem.connect("activate",self.startIndividualCollector,collector)

            stopItem = Gtk.MenuItem("Stop " + collector.name)
            stopItem.connect("activate",self.stopIndividualCollector,collector)

            parseItem = Gtk.MenuItem("Parse " + collector.name + " data")
            parseItem.connect("activate",self.parser,collector)

            # manual collector should only be run by icon
            if(isinstance(collector,engine.collector.AutomaticCollector)):
                menu.append(runItem)
                menu.append(stopItem)

            menu.append(parseItem)

            menu.show_all()
            menu.popup(None, None, None, None, event.button, event.time)
            return True

    # Update background colors of collector rows based on isSelected()
    def update_row_colors(self, event, lboxRow):
        self.startall_button.set_sensitive(True)
        self.collectorList.foreach(self.update_row_color)

    # Helper for update_row_colors
    def update_row_color(self,row):
        if(row.is_selected()):
            row.get_style_context().add_class("active-color")
            row.get_style_context().remove_class("inactive-color")
        if(row.is_selected() == False):
            row.get_style_context().remove_class("active-color")
            row.get_style_context().add_class("inactive-color")

    # Perform the designated action (run,stop,parse) for all selected collectors
    def process_active_collectors(self,event,action):

        selected_collectors = self.collectorList.get_selected_rows()

        if(selected_collectors.__len__() == 0):
            print("No collectors selected...")

        for i, c in enumerate(selected_collectors):
            collector = self.engine.get_collector(c.get_name())
            if(self.currentConfigWindow != None and self.currentConfigWindow.get_name() == collector.name):
                self.currentConfigWindow.set_sensitive(collector.is_running())
                # Config window should NOT be editable IF collector is running
            if collector.is_enabled() and isinstance(collector, engine.collector.AutomaticCollector):
                if(action == Action.RUN):
                    self.startall_button.set_sensitive(False)
                    self.stopall_button.set_sensitive(True)
                    collector.run()
                if(action == Action.STOP):
                    self.startall_button.set_sensitive(True)
                    self.stopall_button.set_sensitive(False)
                    collector.terminate()
            if(action == Action.PARSE):
                collector.parser.parse()

    def create_collector_bbox(self, collector):
        frame = Gtk.Frame()

        if collector.is_enabled():
            layout = Gtk.ButtonBoxStyle.SPREAD
            spacing = 10

            bbox = Gtk.HButtonBox()
            bbox.set_border_width(1)
            bbox.set_layout(layout)
            bbox.set_spacing(spacing)
            frame.add(bbox)

            startCollectorButton = Gtk.Button('Start Collector')
            startCollectorButton.connect("clicked", self.startIndividualCollector, collector)
            startCollectorButton.set_sensitive(not isinstance(collector, engine.collector.ManualCollector))
            bbox.add(startCollectorButton)

            stopCollectorButton = Gtk.Button('Stop Collector')
            stopCollectorButton.connect("clicked", self.stopIndividualCollector, collector)
            stopCollectorButton.set_sensitive(not isinstance(collector, engine.collector.ManualCollector))
            bbox.add(stopCollectorButton)

            parseButton = Gtk.Button('Parse Data')
            parseButton.connect("clicked", self.parser, collector)
            bbox.add(parseButton)
        else:
            label = Gtk.Label(label="Collector Disabled")
            frame.add(label)

        return frame

    def startall_collectors(self, button):
        self.collectorList.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        self.stopall_button.set_sensitive(True)
        self.startall_button.set_sensitive(False)
        self.status_context_menu.tray_ind.set_icon(Gtk.STOCK_MEDIA_RECORD)
        self.status_context_menu.stopall_menu_item.set_sensitive(True)
        self.status_context_menu.startall_menu_item.set_sensitive(False)
        i = 0.0
        pb = ProgressBar()
        while Gtk.events_pending():
            Gtk.main_iteration()

        for collector in self.engine.collectors:
            if collector.is_enabled() and isinstance(collector, engine.collector.AutomaticCollector):
                collector.run()
                self.update_collector_status(Action.RUN,collector.name)
                if(self.currentConfigWindow != None):
                    self.currentConfigWindow.set_sensitive(False)
            pb.setValue(i / len(self.engine.collectors))
            pb.pbar.set_text("Stopping " + collector.name)
            while Gtk.events_pending():
                Gtk.main_iteration()
            i += 1
            if(i == len(self.engine.collectors)):
                pb.setValue(100)
            pb.destroy()
        #if not pb.emit("delete-event", Gdk.Event(Gdk.DELETE)):
            #pb.destroy()

    def update_collector_status(self,action,collectorName):
        row = filter(lambda r: r.get_name() == collectorName, self.collectorList.get_children())
        if(row.__len__() > 0):
            collectorRow = row.pop()
            if(action == Action.RUN):
                self.collectorList.select_row(collectorRow)
            if(action == Action.STOP):
                self.collectorList.unselect_row(collectorRow)
            self.update_row_color(collectorRow)

    def stopall_collectors(self, button):
        self.collectorList.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.stopall_button.set_sensitive(False)
        self.startall_button.set_sensitive(True)
        self.status_context_menu.tray_ind.set_icon(Gtk.STOCK_NO)
        self.status_context_menu.stopall_menu_item.set_sensitive(False)
        self.status_context_menu.startall_menu_item.set_sensitive(True)
        i = 0.0
        pb = ProgressBar()
        while Gtk.events_pending():
            Gtk.main_iteration()

        for collector in self.engine.collectors:
            if collector.is_enabled() and isinstance(collector, engine.collector.AutomaticCollector):
                collector.terminate()
                self.update_collector_status(Action.STOP,collector.name)
                if(self.currentConfigWindow != None):
                    self.currentConfigWindow.set_sensitive(True)
            pb.setValue(i / len(self.engine.collectors))
            pb.pbar.set_text("Stopping " + collector.name)
            while Gtk.events_pending():
                Gtk.main_iteration()
            i += 1
            if (i == len(self.engine.collectors)):
                pb.setValue(100)
            pb.destroy()
            # if not pb.emit("delete-event", Gdk.Event(Gdk.DELETE)):
            # pb.destroy()

    def parse_all(self, event):
        i = 0.0
        pb = ProgressBar()
        while Gtk.events_pending():
            Gtk.main_iteration()

        for collector in self.engine.collectors:
            collector.parser.parse()
            pb.setValue(i/len(self.engine.collectors))
            pb.pbar.set_text("Parsing " + collector.name)
            while Gtk.events_pending():
                Gtk.main_iteration()
            i += 1
        if not pb.emit("delete-event", Gdk.Event(Gdk.DELETE)):
            pb.destroy()

        alert = Gtk.MessageDialog(self, Gtk.DialogFlags.DESTROY_WITH_PARENT, Gtk.MessageType.INFO,
                                      Gtk.ButtonsType.CLOSE, "Parsing complete")
        alert.run()
        alert.destroy()

    def close_all(self, event):
        for collector in self.engine.collectors:
            if collector.is_enabled:
               collector.terminate()
        os._exit(0)

    def parser(self, event, collector):
        collector.parser.parse()

    def stopIndividualCollector(self, event, collector):
        if (self.currentConfigWindow != None and self.currentConfigWindow.get_name() == collector.name):
            self.currentConfigWindow.set_sensitive(collector.is_running())
        collector.terminate()

    def startIndividualCollector(self, event, collector):
        if (self.currentConfigWindow != None and self.currentConfigWindow.get_name() == collector.name):
            self.currentConfigWindow.set_sensitive(collector.is_running())
        collector.run()

    def show_confirmation_dialog(self, msg):
        dialog = Gtk.MessageDialog(self, Gtk.DialogFlags.DESTROY_WITH_PARENT, Gtk.MessageType.INFO,
                                      Gtk.ButtonsType.YES_NO, msg)
        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.YES:
            return True

        return False


