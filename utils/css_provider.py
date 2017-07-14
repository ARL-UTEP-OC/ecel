import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import definitions

class CssProvider:
    def __init__(self, css_file_name):
        self.cssProvider = Gtk.CssProvider()
        self.cssProvider.load_from_path(definitions.PLUGIN_CSS_DIR + css_file_name)
        screen = Gdk.Screen.get_default()
        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen, self.cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER)