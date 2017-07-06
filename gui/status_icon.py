# For GUI
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import engine.collector
from _version import __version__


class CustomSystemTrayIcon:

    def __init__(self, app_engine, gui):
        menu = Gtk.Menu()

        # show main application
        main_application_menu_item = Gtk.MenuItem("Main Application")
        main_application_menu_item.show()
        menu.append(main_application_menu_item)
        main_application_menu_item.connect('activate', self.show_main_gui, gui)

        #separator
        sep0 = Gtk.SeparatorMenuItem()
        sep0.show()
        menu.append(sep0)

        for collector in app_engine.collectors:
            if isinstance(collector, engine.collector.ManualCollector):
                menu_item_collector = Gtk.MenuItem(collector.command_description)
                menu.append(menu_item_collector)
                menu_item_collector.connect('activate', self.run_collector, collector)

        #separator
        sep1 = Gtk.SeparatorMenuItem()
        sep1.show()
        menu.append(sep1)

        # show about_menu_item dialog
        self.startall_menu_item = Gtk.MenuItem("Start All Collectors")
        self.startall_menu_item.show()
        menu.append(self.startall_menu_item)
        self.startall_menu_item.connect('activate', gui.startall_collectors)

        # show about_menu_item dialog
        self.stopall_menu_item = Gtk.MenuItem("Stop All Collectors")
        self.stopall_menu_item.show()
        menu.append(self.stopall_menu_item)
        self.stopall_menu_item.connect('activate', gui.stopall_collectors)
        self.stopall_menu_item.set_sensitive(False)

        #separator
        sep2 = Gtk.SeparatorMenuItem()
        sep2.show()
        menu.append(sep2)

        # show about_menu_item dialog
        about_menu_item = Gtk.MenuItem("About")
        about_menu_item.show()
        menu.append(about_menu_item)
        about_menu_item.connect('activate', self.show_about_dialog)

        # add quit_menu_item item
        quit_menu_item = Gtk.MenuItem("Quit")
        quit_menu_item.show()
        menu.append(quit_menu_item)
        quit_menu_item.connect('activate', self.kill_me, app_engine)

        #self.tray_ind = appindicator.Indicator("ECEL", Gtk.STOCK_NO, appindicator.CATEGORY_SYSTEM_SERVICES)
        #self.tray_ind.set_status(appindicator.STATUS_ACTIVE)
        #self.tray_ind.set_menu(menu)

        menu.show_all()

    def run_collector(self, event, collector):
        collector.run()

    # Simple pop up widget that shows some information about the program
    def show_about_dialog(self, widget):
        about_dialog = Gtk.AboutDialog()
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_icon_name("Evaluator-Centric and Extensible Logger v%s" % (__version__))
        about_dialog.set_name('ECEL')
        about_dialog.set_version(__version__)
        about_dialog.set_comments(("ECEL was developed as the result of a collaborative research project between the US Army Research Laboratory and the University of Texas at El Paso."))
        about_dialog.run()
        about_dialog.destroy()

    def kill_me(self, event, app_engine):
        for collector in app_engine.collectors:
            if collector.is_enabled:
               collector.terminate()
        os._exit(0)

    def show_main_gui(self, event, gui):
        gui.show_gui()
