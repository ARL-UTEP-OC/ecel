import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import signal
from engine.engine import Engine
from gui.main_gui import MainGUI

engine = Engine()

if __name__ == "__main__":
    Gdk.threads_init()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    MainGUI(engine)
    Gtk.main()