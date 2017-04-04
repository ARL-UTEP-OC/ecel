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
        main_application = gtk.MenuItem("Main Application")
        main_application.show()
        menu.append(main_application)
        main_application.connect('activate', self.show_my_gui, gui)

        # add manual screenshot functionality
        # TODO: This should be loaded dynamically based on plugins labeled to be manual
        screen_shot = gtk.MenuItem("Take Manual ScreenShot")
        ms = engine.get_plugin("manualscreenshot")
        if ms.is_enabled:
            screen_shot.show()
            menu.append(screen_shot)
            screen_shot.connect('activate', self.take_screen)
        #screen_shot.connect("activate", t)

        # show about dialog
        about = gtk.MenuItem("About")
        about.show()
        menu.append(about)
        about.connect('activate', self.show_about_dialog)

        # add quit item
        quit = gtk.MenuItem("Quit")
        quit.show()
        menu.append(quit)
        quit.connect('activate', self.kill_me, engine)

        self.tray_ind = appindicator.Indicator("example-simple-client", "starred", appindicator.CATEGORY_APPLICATION_STATUS)
        self.tray_ind.set_status(appindicator.STATUS_ACTIVE)
        self.tray_ind.set_menu(menu)

    # Simple pop up widget that shows some information about the program
    def show_about_dialog(self, widget): #TODO: Change info?
        about_dialog = gtk.AboutDialog()
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_icon_name("Evaluator-Centric and Extensible Logger v%s" % (__version__))
        about_dialog.set_name('ECEL')
        about_dialog.set_version(__version__)
        about_dialog.set_comments(("This software is a result of the ARL/UTEP Open Campus Initiative."))
        about_dialog.run()
        about_dialog.destroy()

    def take_screen(event_button, event):
        takeshoot.CaptureScreen()
        #CustomSystemTrayIcon.core1.get_plugin("manualscreenshot").run()

    def kill_me(self, event, engine):
        for plugin in engine.plugins:
            if plugin.is_enabled:
               plugin.terminate()
        os._exit(0)

    def show_my_gui(self, event, gui):
        gui()
