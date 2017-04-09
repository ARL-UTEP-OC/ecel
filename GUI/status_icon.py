# For GUI
import gtk
import os
import appindicator

from plugins.collectors.manualscreenshot import takeshoot
from _version import __version__

class CustomSystemTrayIcon:

    def __init__(self, engine, gui):
        menu = gtk.Menu()

        # show main application
        main_application_menu_item = gtk.MenuItem("Main Application")
        main_application_menu_item.show()
        menu.append(main_application_menu_item)
        main_application_menu_item.connect('activate', self.show_my_gui, gui)

        #separator
        sep0 = gtk.SeparatorMenuItem()
        sep0.show()
        menu.append(sep0)

        # add manual screenshot functionality
        # TODO: This should be loaded dynamically based on plugins labeled to be manual
        screen_shot_menu_item = gtk.MenuItem("Take Manual ScreenShot")
        ms = engine.get_plugin("manualscreenshot")
        if ms.is_enabled:
            screen_shot_menu_item.show()
            menu.append(screen_shot_menu_item)
            screen_shot_menu_item.connect('activate', self.take_screen)

        #separator
        sep1 = gtk.SeparatorMenuItem()
        sep1.show()
        menu.append(sep1)

        # show about_menu_item dialog
        self.startall_menu_item = gtk.MenuItem("Start All Collectors")
        self.startall_menu_item.show()
        menu.append(self.startall_menu_item)
        self.startall_menu_item.connect('activate', gui.startall_collectors)

        # show about_menu_item dialog
        self.stopall_menu_item = gtk.MenuItem("Stop All Collectors")
        self.stopall_menu_item.show()
        menu.append(self.stopall_menu_item)
        self.stopall_menu_item.connect('activate', gui.stopall_collectors)
        self.stopall_menu_item.set_sensitive(False)

        #separator
        sep2 = gtk.SeparatorMenuItem()
        sep2.show()
        menu.append(sep2)

        # show about_menu_item dialog
        about_menu_item = gtk.MenuItem("About")
        about_menu_item.show()
        menu.append(about_menu_item)
        about_menu_item.connect('activate', self.show_about_dialog)

        # add quit_menu_item item
        quit_menu_item = gtk.MenuItem("Quit")
        quit_menu_item.show()
        menu.append(quit_menu_item)
        quit_menu_item.connect('activate', self.kill_me, engine)

        self.tray_ind = appindicator.Indicator("ECEL", gtk.STOCK_NO, appindicator.CATEGORY_SYSTEM_SERVICES)
        self.tray_ind.set_status(appindicator.STATUS_ACTIVE)
        self.tray_ind.set_menu(menu)

    # Simple pop up widget that shows some information about the program
    def show_about_dialog(self, widget):
        about_dialog = gtk.AboutDialog()
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_icon_name("Evaluator-Centric and Extensible Logger v%s" % (__version__))
        about_dialog.set_name('ECEL')
        about_dialog.set_version(__version__)
        about_dialog.set_comments(("ECEL was developed as the result of a collaborative research project between the US Army Research Laboratory and the University of Texas at El Paso."))
        about_dialog.run()
        about_dialog.destroy()

    def take_screen(event_button, event):
        takeshoot.CaptureScreen()

    def kill_me(self, event, engine):
        for plugin in engine.plugins:
            if plugin.is_enabled:
               plugin.terminate()
        os._exit(0)

    def show_my_gui(self, event, gui):
        gui.show_gui()
