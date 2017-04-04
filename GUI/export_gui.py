import gtk
import os
import shutil
import time
from os.path import expanduser
from engine.archiver.zipFormat import zip
from engine.archiver.tarFormat import tar

RAW="raw"
COMPRESSED="compressed"
PARSED="parsed"

EXPORT_DIRNAME="ecel-export%TIME%"

class Export_GUI(gtk.Window):
    def __init__(self, parent):
        super(Export_GUI, self).__init__()

        self.main_gui = parent
        self.collectors_dir = self.main_gui.engine.collectors_directory

        self.set_title("Export Plugin Data")
        self.set_modal(True)
        self.set_transient_for(self.main_gui)
        self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.set_size_request(275, 250)
        self.set_resizable(False)

        self.checkbutton_export_raw = gtk.CheckButton("All raw data")
        self.checkbutton_export_raw.set_active(True)
        self.checkbutton_export_compressed = gtk.CheckButton("All compressed data")
        self.checkbutton_export_compressed.set_active(True)
        self.checkbutton_export_parsed = gtk.CheckButton("All parsed data")
        self.checkbutton_export_parsed.set_active(True)

        self.checkbutton_compress_export = gtk.CheckButton("Compress exported files:")
        self.checkbutton_compress_export.set_active(True)
        self.checkbutton_compress_export.connect("toggled", self.checkbutton_compress_export_toggled)
        self.radiobutton_compress_export_format_zip = gtk.RadioButton(None, ".zip format")
        self.radiobutton_compress_export_format_zip.set_active(True)
        self.radiobutton_compress_export_format_tar = gtk.RadioButton(self.radiobutton_compress_export_format_zip, ".tar.bz2 format")

        self.entry_selected_folder = gtk.Entry()
        self.entry_selected_folder.set_text(expanduser("~"))
        button_select_folder = gtk.ToolButton(gtk.image_new_from_file(os.path.join(os.path.join(os.getcwd(), "GUI"),"open_small.png")))
        button_select_folder.connect("clicked", self.select_folder)

        button_export = gtk.Button("Export")
        button_export.connect("clicked", self.export)
        button_cancel = gtk.Button("Cancel")
        button_cancel.connect("clicked", self.close_export_dialog)

        vbox = gtk.VBox()
        frame_exporttype = gtk.Frame("Export:")
        vbox_exporttype = gtk.VBox()
        vbox_exporttype.pack_start(self.checkbutton_export_raw)
        vbox_exporttype.pack_start(self.checkbutton_export_compressed)
        vbox_exporttype.pack_start(self.checkbutton_export_parsed)
        frame_exportoptions = gtk.Frame("Export Options:")
        vbox_exportoptions = gtk.VBox()
        vbox_exportoptions.pack_start(self.checkbutton_compress_export)
        hbox_exportformat = gtk.HBox()
        hbox_exportformat.pack_start(self.radiobutton_compress_export_format_zip)
        hbox_exportformat.pack_start(self.radiobutton_compress_export_format_tar)
        vbox_exportoptions.pack_start(hbox_exportformat)
        frame_exportto = gtk.Frame("Export To:")
        hbox_exportto = gtk.HBox()
        hbox_exportto.pack_start(self.entry_selected_folder)
        hbox_exportto.pack_start(button_select_folder)
        hbox_okcancel = gtk.HBox()
        hbox_okcancel.pack_start(button_cancel)
        hbox_okcancel.pack_start(button_export)
        frame_exporttype.add(vbox_exporttype)
        frame_exportoptions.add(vbox_exportoptions)
        frame_exportto.add(hbox_exportto)
        vbox.pack_start(frame_exporttype)
        vbox.pack_start(frame_exportoptions)
        vbox.pack_start(frame_exportto)
        vbox.pack_start(hbox_okcancel)

        self.add(vbox)

        self.show_all()

    def checkbutton_compress_export_toggled(self, event):
        if self.checkbutton_compress_export.get_active():
            self.radiobutton_compress_export_format_zip.set_sensitive(True)
            self.radiobutton_compress_export_format_tar.set_sensitive(True)
        else:
            self.radiobutton_compress_export_format_zip.set_sensitive(False)
            self.radiobutton_compress_export_format_tar.set_sensitive(False)

    def select_folder(self, event):
        dialog_select_folder = gtk.FileChooserDialog()
        dialog_select_folder.set_title("Export To")
        dialog_select_folder.set_transient_for(self)
        dialog_select_folder.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        dialog_select_folder.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)
        dialog_select_folder.set_current_folder(self.entry_selected_folder.get_text())

        response = dialog_select_folder.run()
        if response == gtk.RESPONSE_OK:
            self.entry_selected_folder.set_text(dialog_select_folder.get_filename())

        dialog_select_folder.destroy()

    def close_export_dialog(self, event):
        self.hide_all()

    def export(self, event):
        export_base_dir = self.entry_selected_folder.get_text()
        export_raw = self.checkbutton_export_raw.get_active()
        export_compressed = self.checkbutton_export_compressed.get_active()
        export_parsed = self.checkbutton_export_parsed.get_active()

        if not export_base_dir:
            self.show_error_message("Please select a directory to export to.")
            return
        if not os.path.isdir(export_base_dir):
            self.show_error_message("Please select a valid directory to export to.")
            return
        if not export_raw and not export_compressed and not export_parsed:
            self.show_error_message("Please select at least one data type to export.")
            return

        export_dir = os.path.join(export_base_dir, EXPORT_DIRNAME.replace("%TIME%", "_" + str(int(time.time()))))
        export_raw_dir = os.path.join(export_dir, RAW)
        export_compressed_dir = os.path.join(export_dir, COMPRESSED)
        export_parsed_dir = os.path.join(export_dir, PARSED)
        os.makedirs(export_raw_dir)
        os.makedirs(export_compressed_dir)
        os.makedirs(export_parsed_dir)

        for plugin in next(os.walk(self.collectors_dir))[1]:
            plugin_export_raw_dir = os.path.join(export_raw_dir, plugin)
            plugin_export_compressed_dir = os.path.join(export_compressed_dir, plugin)
            plugin_export_parsed_dir = os.path.join(export_parsed_dir, plugin)
            plugin_collector_dir = os.path.join(self.collectors_dir, plugin)
            plugin_collector_raw_dir = os.path.join(plugin_collector_dir, RAW)
            plugin_collector_compressed_dir = os.path.join(plugin_collector_dir, COMPRESSED)
            plugin_collector_parsed_dir = os.path.join(plugin_collector_dir, PARSED)

            if export_raw and os.path.exists(plugin_collector_raw_dir) and os.listdir(plugin_collector_raw_dir):
                shutil.copytree(plugin_collector_raw_dir, plugin_export_raw_dir)
            if export_compressed and os.path.exists(plugin_collector_compressed_dir) and os.listdir(plugin_collector_compressed_dir):
                shutil.copytree(plugin_collector_compressed_dir, plugin_export_compressed_dir)
            if export_parsed and os.path.exists(plugin_collector_parsed_dir) and os.listdir(plugin_collector_parsed_dir):
                shutil.copytree(plugin_collector_parsed_dir, plugin_export_parsed_dir)

        if self.checkbutton_compress_export.get_active():
            export_dir_notime = os.path.join(export_base_dir, EXPORT_DIRNAME.replace("%TIME%", ""))
            if self.radiobutton_compress_export_format_zip.get_active():
                zip(export_dir, export_dir_notime)
            elif self.radiobutton_compress_export_format_tar.get_active():
                tar(export_dir, export_dir_notime)
            shutil.rmtree(export_dir)

        self.hide_all()

    def show_error_message(self, msg):
        alert = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,
                                      gtk.BUTTONS_CLOSE, msg)
        alert.run()
        alert.destroy()
