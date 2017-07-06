import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def show_alert_message(parent_window, msg):
    alert = Gtk.MessageDialog(parent_window, Gtk.DialogFlags.DESTROY_WITH_PARENT, Gtk.MessageType.INFO,
                              Gtk.ButtonsType.CLOSE, msg)
    alert.run()
    alert.destroy()

def show_error_message(parent_window, msg):
    alert = Gtk.MessageDialog(parent_window, Gtk.DialogFlags.DESTROY_WITH_PARENT , Gtk.MessageType.ERROR,
                              Gtk.ButtonsType.CLOSE, msg)
    alert.run()
    alert.destroy()