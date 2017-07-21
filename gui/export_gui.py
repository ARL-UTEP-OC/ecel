import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk
import os
import shutil
import time
import definitions
import utils.gui
from os.path import expanduser
from engine.archiver.zip_format import zip
from engine.archiver.tar_format import tar
from gui.progress_bar import ProgressBar

class ExportGUI(Gtk.Window):
    def __init__(self, parent):
        super(ExportGUI, self).__init__()

        self.main_gui = parent
        self.collectors_dir = definitions.PLUGIN_COLLECTORS_DIR

        self.set_title("Export Plugin Data")
        self.set_modal(True)
        self.set_transient_for(self.main_gui)
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        self.set_size_request(275, 250)
        self.set_resizable(False)

        self.checkbutton_export_raw = Gtk.CheckButton("All raw data")
        self.checkbutton_export_raw.set_active(True)
        self.checkbutton_export_compressed = Gtk.CheckButton("All compressed data")
        self.checkbutton_export_compressed.set_active(True)
        self.checkbutton_export_parsed = Gtk.CheckButton("All parsed data")
        self.checkbutton_export_parsed.set_active(True)

        self.checkbutton_compress_export = Gtk.CheckButton("Compress exported files:")
        self.checkbutton_compress_export.set_active(True)
        self.checkbutton_compress_export.connect("toggled", self.checkbutton_compress_export_toggled)
        self.radiobutton_compress_export_format_zip = Gtk.RadioButton()
        self.radiobutton_compress_export_format_zip.set_label(".zip format")
        self.radiobutton_compress_export_format_zip.set_active(True)
        self.radiobutton_compress_export_format_tar = Gtk.RadioButton().new_with_label_from_widget(self.radiobutton_compress_export_format_zip,".tar.bz2 format")

        self.entry_selected_folder = Gtk.Entry()
        self.entry_selected_folder.set_text(expanduser("~"))
        self.entry_selected_folder.connect("key-release-event", self.on_key_release)
        image = Gtk.Image()
        image.set_from_file(os.path.join(definitions.ICONS_DIR, "open_small.png"))
        image.show()
        button_select_folder = Gtk.ToolButton()
        button_select_folder.set_icon_widget(image)
        button_select_folder.connect("clicked", self.select_folder)

        button_export = Gtk.Button("Export")
        button_export.connect("clicked", self.export)

        button_cancel = Gtk.Button("Cancel")
        button_cancel.connect("clicked", self.close_export_dialog)

        vbox = Gtk.VBox()
        frame_exporttype = Gtk.Frame()
        frame_exporttype.set_label("Export:")
        vbox_exporttype = Gtk.VBox()
        vbox_exporttype.pack_start(self.checkbutton_export_raw, True, True, 0)
        vbox_exporttype.pack_start(self.checkbutton_export_compressed, True, True, 0)
        vbox_exporttype.pack_start(self.checkbutton_export_parsed, True, True, 0)
        frame_exportoptions = Gtk.Frame()
        frame_exportoptions.set_label("Export Options:")
        vbox_exportoptions = Gtk.VBox()
        vbox_exportoptions.pack_start(self.checkbutton_compress_export, True, True, 0)
        hbox_exportformat = Gtk.HBox()
        hbox_exportformat.pack_start(self.radiobutton_compress_export_format_zip, True, True, 0)
        hbox_exportformat.pack_start(self.radiobutton_compress_export_format_tar, True, True, 0)
        vbox_exportoptions.pack_start(hbox_exportformat, True, True, 0)
        frame_exportto = Gtk.Frame()
        hbox_exportto = Gtk.HBox()
        hbox_exportto.pack_start(self.entry_selected_folder, True, True, 0)
        hbox_exportto.pack_start(button_select_folder, True, True, 0)
        hbox_okcancel = Gtk.HBox()
        hbox_okcancel.pack_start(button_cancel, True, True, 0)
        hbox_okcancel.pack_start(button_export, True, True, 0)
        frame_exporttype.add(vbox_exporttype)
        frame_exportoptions.add(vbox_exportoptions)
        frame_exportto.add(hbox_exportto)
        vbox.pack_start(frame_exporttype, True, True, 0)
        vbox.pack_start(frame_exportoptions, True, True, 0)
        vbox.pack_start(frame_exportto, True, True, 0)
        vbox.pack_start(hbox_okcancel, True, True, 0)

        self.add(vbox)

        self.show_all()

    def on_key_release(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval)
        if keyname == "KP_Enter" or keyname == "Return":
            self.export(event)

    def checkbutton_compress_export_toggled(self, event):
        if self.checkbutton_compress_export.get_active():
            self.radiobutton_compress_export_format_zip.set_sensitive(True)
            self.radiobutton_compress_export_format_tar.set_sensitive(True)
        else:
            self.radiobutton_compress_export_format_zip.set_sensitive(False)
            self.radiobutton_compress_export_format_tar.set_sensitive(False)

    def select_folder(self, event):
        dialog_select_folder = Gtk.FileChooserDialog()
        dialog_select_folder.set_title("Export To")
        dialog_select_folder.set_transient_for(self)
        dialog_select_folder.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        dialog_select_folder.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        dialog_select_folder.set_current_folder(self.entry_selected_folder.get_text())

        response = dialog_select_folder.run()
        if response == Gtk.ResponseType.OK:
            self.entry_selected_folder.set_text(dialog_select_folder.get_filename())

        dialog_select_folder.destroy()

    def close_export_dialog(self, event):
        self.hide()

    def export(self, event):
        export_base_dir = self.entry_selected_folder.get_text()
        export_raw = self.checkbutton_export_raw.get_active()
        export_compressed = self.checkbutton_export_compressed.get_active()
        export_parsed = self.checkbutton_export_parsed.get_active()

        if not export_base_dir:
            utils.gui.show_error_message(self, "Please select a directory to export to.")
            return
        if not os.path.isdir(export_base_dir):
            utils.gui.show_error_message(self, "Please select a valid directory to export to.")
            return
        if not export_raw and not export_compressed and not export_parsed:
            utils.gui.show_error_message(self, "Please select at least one data type to export.")
            return

        export_dir = os.path.join(export_base_dir, definitions.PLUGIN_COLLECTORS_EXPORT_DIRNAME.replace(
            definitions.TIMESTAMP_PLACEHOLDER, "_" + str(int(time.time()))))
        export_raw_dir = os.path.join(export_dir, definitions.PLUGIN_COLLECTORS_OUTPUT_DIRNAME)
        export_compressed_dir = os.path.join(export_dir, definitions.PLUGIN_COLLECTORS_COMPRESSED_DIRNAME)
        export_parsed_dir = os.path.join(export_dir, definitions.PLUGIN_COLLECTORS_PARSED_DIRNAME)
        os.makedirs(export_raw_dir)
        os.makedirs(export_compressed_dir)
        os.makedirs(export_parsed_dir)

        progress = 0
        pb = ProgressBar()
        while Gtk.events_pending():
            Gtk.main_iteration()

        for plugin in next(os.walk(self.collectors_dir))[1]:
            plugin_export_raw_dir = os.path.join(export_raw_dir, plugin)
            plugin_export_compressed_dir = os.path.join(export_compressed_dir, plugin)
            plugin_export_parsed_dir = os.path.join(export_parsed_dir, plugin)
            plugin_collector_dir = os.path.join(self.collectors_dir, plugin)
            plugin_collector_raw_dir = os.path.join(plugin_collector_dir, definitions.PLUGIN_COLLECTORS_OUTPUT_DIRNAME)
            plugin_collector_compressed_dir = os.path.join(plugin_collector_dir, definitions.PLUGIN_COLLECTORS_COMPRESSED_DIRNAME)
            plugin_collector_parsed_dir = os.path.join(plugin_collector_dir, definitions.PLUGIN_COLLECTORS_PARSED_DIRNAME)

            if export_raw and os.path.exists(plugin_collector_raw_dir) and os.listdir(plugin_collector_raw_dir):
                shutil.copytree(plugin_collector_raw_dir, plugin_export_raw_dir)
            if export_compressed and os.path.exists(plugin_collector_compressed_dir) and os.listdir(plugin_collector_compressed_dir):
                shutil.copytree(plugin_collector_compressed_dir, plugin_export_compressed_dir)
            if export_parsed and os.path.exists(plugin_collector_parsed_dir) and os.listdir(plugin_collector_parsed_dir):
                shutil.copytree(plugin_collector_parsed_dir, plugin_export_parsed_dir)
            pb.setValue((progress / len(next(os.walk(self.collectors_dir))[1]))*.8)
            pb.pbar.set_text("Copying files " + plugin)
            while Gtk.events_pending():
                Gtk.main_iteration()
            progress += 1

        if self.checkbutton_compress_export.get_active():
            export_dir_notime = os.path.join(export_base_dir, definitions.PLUGIN_COLLECTORS_EXPORT_DIRNAME.replace(
                definitions.TIMESTAMP_PLACEHOLDER, ""))
            pb.pbar.set_text("Compressing data to " + export_dir)
            pb.setValue(.85)
            while Gtk.events_pending():
                Gtk.main_iteration()
            if self.radiobutton_compress_export_format_zip.get_active():
                zip(export_dir, export_dir_notime)
            elif self.radiobutton_compress_export_format_tar.get_active():
                tar(export_dir, export_dir_notime)
            pb.pbar.set_text("Cleaning up " + export_dir)
            pb.setValue(.9)
            while Gtk.events_pending():
                Gtk.main_iteration()
            shutil.rmtree(export_dir)
        if not pb.emit("delete-event", Gdk.Event()):
            pb.destroy()

        utils.gui.show_alert_message(self, "Export complete")

        self.hide()
