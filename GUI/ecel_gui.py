import gtk
import os
import shutil
import subprocess
import shlex

import status_icon
from Config import Runner
from GUI.export_gui import Export_GUI
from _version import __version__

PYKEYLOGGER = "pykeylogger"

class ECEL_GUI(gtk.Window):
    def __init__(self, engine):
        self.devnull = open(os.devnull, 'w')
        super(ECEL_GUI, self).__init__()

        #create tooltips
        self.tooltips = gtk.Tooltips()

        # Call function to me System Tray Icon
        self.test = status_icon.CustomSystemTrayIcon(engine, self.show_gui)
        #self.set_keep_above(False)
        # Set Title and Size of Main Window Frame
        self.set_title("Evaluator-Centric and Extensible Logger v%s" % (__version__))
        self.set_size_request(850, 500)
        self.set_position(gtk.WIN_POS_CENTER)
        self.engine = engine
        self.connect("delete-event", self.hide_on_delete)
        Runner.scaffold_initial_files()

        # Creating Tool Bar
        toolbar = gtk.Toolbar()
        toolbar.set_style(gtk.TOOLBAR_ICONS)

        #open_button = gtk.ToolButton(gtk.image_new_from_file(os.path.join(os.path.join(os.getcwd(), "GUI"), "open.png")))
        #open_button.connect("clicked", self.callback)
        #pause_button = gtk.ToolButton(gtk.image_new_from_file(os.path.join(os.path.join(os.getcwd(), "GUI"),"pause.png")))
        #pause_button.connect("clicked", self.pause_plugin)
        self.start_button = gtk.ToolButton(gtk.image_new_from_file(os.path.join(os.path.join(os.getcwd(), "GUI"),"start.png")))
        self.tooltips.set_tip(self.start_button, "Start All Plugins")
        self.start_button.connect("clicked", self.start_plugin)

        self.stop_button = gtk.ToolButton(gtk.image_new_from_file(os.path.join(os.path.join(os.getcwd(), "GUI"),"stop.png")))
        self.tooltips.set_tip(self.stop_button, "Stop All Plugins")
        self.stop_button.connect("clicked", self.stop_plugin)
        self.stop_button.set_sensitive(False)

        separator = gtk.SeparatorToolItem()

        self.json_button = gtk.ToolButton(gtk.image_new_from_file(os.path.join(os.path.join(os.getcwd(), "GUI"),"json.png")))
        self.tooltips.set_tip(self.json_button, "Parse All Captured to JSON")
        self.json_button.connect("clicked", self.parse_all, engine)

        self.export_button = gtk.ToolButton(gtk.image_new_from_file(os.path.join(os.path.join(os.getcwd(), "GUI"),"export.png")))
        self.tooltips.set_tip(self.export_button, "Export Plugin Data")
        self.export_button.connect("clicked", self.export)

        #hide_button = gtk.ToolButton(gtk.image_new_from_file(os.path.join(os.path.join(os.getcwd(), "GUI"),"hide.png")))
        #hide_button.connect("clicked", self.hide_gui)
        #toolbar.insert(open_button, 0)
        toolbar.insert(self.start_button, 0)
        #toolbar.insert(pause_button, 2)
        toolbar.insert(self.stop_button, 1)
        toolbar.insert(separator, 2)
        toolbar.insert(self.json_button, 3)
        toolbar.insert(self.export_button, 4)
        #toolbar.insert(hide_button, 4)

        # Creating a Vertical Container To Add Widgets To
        vbox = gtk.VBox(False, 2)

        # Adding the Vertical Container To Main Window Frame
        self.add(vbox)
        self.connect("destroy", self.close_all)


        # Create File Menu Bar
        top_menu_bar = gtk.MenuBar()

        # Create menu that will be displayed in the GUI via the typical File drop down list
        filemenu = gtk.Menu()
        file_menu = gtk.MenuItem("File")
        file_menu.set_submenu(filemenu)
        top_menu_bar.append(file_menu)

        engineConfiguration = gtk.MenuItem("Engine Configuration")
        engineConfiguration.connect("activate", Runner.call_engine_config)
        filemenu.append(engineConfiguration)

        pluginConfiguration = gtk.MenuItem("Plugin Configuration")
        pluginConfiguration.connect("activate", Runner.call_plugins_config)
        filemenu.append(pluginConfiguration)

        # have to be appended in reverse order for some reason.
        exit = gtk.MenuItem("Exit")
        exit.connect("activate", self.close_all)
        filemenu.append(exit)

        # Pack both Widgets on Screen
        vbox.pack_start(top_menu_bar, False, False, 0)
        vbox.pack_start(toolbar, False, False, 0)

        # Load Plugins On To Screen
        i=1
        for plugin in engine.plugins:
            print "%d) %s" % (i, plugin.name)
            i = i+1
            vbox.pack_start(self.create_bbox(plugin),True, True, 5)
        self.show_all()
    # To be used by the status icon Main Application, it will bring the GUI back to the foreground
    def show_gui(self):
        self.present()
        self.show_all()

    # Will be accessed via the Hide Gui button.
    def hide_gui(self, event):
        self.hide()

    def parse_all(self, event, engine):
        for plugin in engine.plugins:
            engine.parsers[plugin.name].parse()

    def export(self, event):
        Export_GUI(self)

    def create_bbox(self, plugin):
        layout = gtk.BUTTONBOX_SPREAD
        spacing = 10
        frame = gtk.Frame(plugin.name)

        bbox = gtk.HButtonBox()
        bbox.set_border_width(1)
        frame.add(bbox)

        # Get value of plugin "enabled status" from the associated json file.
        # hard coded right now, I want to have the "title" from the parameter be used for the path\config.json

        # Set the appearance of the Button Box
        bbox.set_layout(layout)
        bbox.set_spacing(spacing)


        # enableButton = gtk.Button(str(plugin.is_enabled))
        # enableButton.connect("clicked", self.enableButton_clicked)
        # enableButton.set_sensitive(False)
        # bbox.add(enableButton)

        startPluginButton = gtk.Button('Start Plugin')
        startPluginButton.connect("clicked", self.startIndividualPlugin, plugin)
        if plugin.is_enabled == False:
            startPluginButton.set_sensitive(False)
        bbox.add(startPluginButton)

        stopPluginButton = gtk.Button('Stop Plugin')
        stopPluginButton.connect("clicked", self.stopIndividualPlugin, plugin)
        if plugin.is_enabled == False:
            stopPluginButton.set_sensitive(False)
        bbox.add(stopPluginButton)

        parseButton = gtk.Button('Parse')
        parseButton.connect("clicked", self.parser, plugin.name)
        bbox.add(parseButton)

        if plugin.name == PYKEYLOGGER:
            appConfigButton = gtk.Button('Application Configuration')
            appConfigButton.connect("clicked", self.open_control_panel, plugin)
            bbox.add(appConfigButton)
        else:
            appConfigButton = gtk.Button('Application Configuration')
            appConfigButton.set_sensitive(False)
            bbox.add(appConfigButton)


        return frame

    def enableButton_clicked(self, button):
        print button.get_label()
        if button.get_label() == "Enabled":
            button.set_label("Disabled")


    def start_plugin(self, button):
        button.set_sensitive(False)
        self.stop_button.set_sensitive(True)
        for plugin in self.engine.plugins:
            if plugin.is_enabled:
                plugin.run()

    def stop_plugin(self, button):
        self.start_button.set_sensitive(True)
        button.set_sensitive(False)
        for plugin in self.engine.plugins:
            if plugin.is_enabled:
               plugin.terminate()

    def pause_plugin(self, button):
        for plugin in self.engine.plugins:
            if plugin.suspend():
                plugin.resume()
            else:
                plugin.suspend()

    def close_all(self, event):
        for plugin in self.engine.plugins:
            if plugin.is_enabled:
               plugin.terminate()
        os._exit(0)


    def parser(self, event, *args):
        self.engine.parsers[args[0]].parse()

    def open_control_panel(self, event, plugin):
        subprocess.Popen(shlex.split("python controlpanel.py"),
                             shell=False,
                             cwd=plugin.base_dir,
                             stdout=self.devnull,
                             stderr=self.devnull)

    def callback(self, widget, data=None):
        filechooser = gtk.FileChooserDialog('Select Plugin Directory', None,
                                            gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                            ('Cancel', 1, 'Open', 2))
        ans = filechooser.run()
        if ans == 2:
            new_plugin_path = os.path.normpath(filechooser.get_current_folder())
            folder = os.path.basename(new_plugin_path)
            if os.name == 'nt':
                shutil.copytree(new_plugin_path, os.path.join(os.getcwd(), "plugins\\collectors\\" + folder))
            elif os.name == 'posix':
                shutil.copytree(new_plugin_path, os.path.join(os.getcwd(), "plugins//collectors//" + folder))
            filechooser.destroy()
        else:
            filechooser.destroy()

    def stopIndividualPlugin(self, event, plugin):
        plugin.terminate()

    def startIndividualPlugin(self, event, plugin):
        plugin.run()

    def copy(src, dst, event):
        if os.path.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))
        shutil.copytree(src, dst)