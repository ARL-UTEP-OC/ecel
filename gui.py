import gtk
import signal
from core.core import Core
from GUI.ecel_gui import ECEL_GUI

core = Core()

if __name__ == "__main__":
    gtk.threads_init()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    ECEL_GUI(core)
    gtk.main()
