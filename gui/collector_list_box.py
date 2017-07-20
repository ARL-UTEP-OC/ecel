import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk
from utils.css_provider import CssProvider
from utils.collector_action import Action
import engine.collector
import definitions

class CollectorListBox(Gtk.ListBox):

    def __init__(self, engine, main_gui):
        super(CollectorListBox,self).__init__()

        self.engine = engine
        self.numCollectors = self.engine.get_collector_length()
        self.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.attached_gui = main_gui
        self.css = CssProvider("widget_styles.css")

        self.connect("row-activated",self.update_row_colors)
        # Enable multiple collector selection when (SHIFT + CTRL) occurs (selection mode == MULTIPLE)
        self.connect("key-press-event",self.ctrl_shift_enable_multiple_collector_selection)
        # Makes the next click revert back to single selection mode when (SHIFT + CTRL) released
        self.connect("key-release-event",self.ctrl_shift_disable_multiple_collector_selection)

        for i, collector in enumerate(self.engine.collectors):
            self.add(self.create_collector_row(collector))

    def ctrl_shift_enable_multiple_collector_selection(self, listBox, event):
        modifiers = Gtk.accelerator_get_default_mod_mask()
        shift_ctrl_pressed = ((event.state & modifiers) == Gdk.ModifierType.CONTROL_MASK) | (event.state & modifiers) == Gdk.ModifierType.SHIFT_MASK
        ctrl_shift_pressed = ((event.state & modifiers) == Gdk.ModifierType.SHIFT_MASK) | (event.state & modifiers) == Gdk.ModifierType.CONTROL_MASK

        if(shift_ctrl_pressed | ctrl_shift_pressed): # Can now handle simultaneous (CTRL + SHIFT) presses
            self.set_selection_mode(Gtk.SelectionMode.MULTIPLE)

            # When (SHIFT + CTRL) keys are released, revert back to single selection on next click

    def ctrl_shift_disable_multiple_collector_selection(self, listBox, event):
        modifiers = Gtk.accelerator_get_default_mod_mask()
        if (((event.state & modifiers) == Gdk.ModifierType.CONTROL_MASK) == False
            | ((event.state & modifiers) == Gdk.ModifierType.SHIFT_MASK) == False):
            # Next click will reset collector list to single selection mode
            # Next click because if we just reset to single selection now...
            # ...any selected collectors would be unselected automatically
            self.connect("button-press-event", self.enable_single_selection)

            # Revert back to single selection only for collectors

    def enable_single_selection(self, lBox, event):
        # Left click
        if (event.button == Gdk.BUTTON_PRIMARY):
            # Unselect all rows
            self.unselect_all()
            # Reset selection mode to single
            self.set_selection_mode(Gtk.SelectionMode.SINGLE)
            # Disable this handler so that multiple selection is possible again in the future.
            self.disconnect_by_func(self.enable_single_selection)

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
        if(event.button == Gdk.BUTTON_PRIMARY):
            if(self.get_selection_mode() == Gtk.SelectionMode.SINGLE):
                self.attached_gui.create_config_window(event,collector)
        if(event.button == Gdk.BUTTON_SECONDARY): # right click
            self.show_collector_popup_menu(event,collector)

    def show_collector_popup_menu(self, event, collector):
        menu = Gtk.Menu()

        runItem = Gtk.MenuItem("Run " + collector.name)
        runItem.connect("activate", self.attached_gui.startIndividualCollector, collector)

        stopItem = Gtk.MenuItem("Stop " + collector.name)
        stopItem.connect("activate", self.attached_gui.stopIndividualCollector, collector)

        parseItem = Gtk.MenuItem("Parse " + collector.name + " data")
        parseItem.connect("activate", self.attached_gui.parser, collector)

        # manual collector should only be run by icon
        if (isinstance(collector, engine.collector.AutomaticCollector)):
            menu.append(runItem)
            menu.append(stopItem)

        menu.append(parseItem)

        menu.show_all()
        menu.popup(None, None, None, None, event.button, event.time)

        return True

    # Update background colors of collector rows based on isSelected()
    def update_row_colors(self, event, lboxRow):
        self.foreach(self.update_row_color)

    # Helper for update_row_colors
    def update_row_color(self,row):
        if(row.is_selected()):
            row.get_style_context().add_class("active-color")
            row.get_style_context().remove_class("inactive-color")
        if(row.is_selected() == False):
            row.get_style_context().remove_class("active-color")
            row.get_style_context().add_class("inactive-color")

    def update_collector_status(self, action, collectorName):
        row = filter(lambda r: r.get_name() == collectorName, self.get_children())
        if (row.__len__() > 0):
            collectorRow = row.pop()
            if (action == Action.RUN):
                self.select_row(collectorRow)
            if (action == Action.STOP):
                self.unselect_row(collectorRow)
            self.update_row_color(collectorRow)

