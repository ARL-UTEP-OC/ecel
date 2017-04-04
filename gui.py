import gtk
import signal
from engine.engine import Engine
from GUI.ecel_gui import ECEL_GUI

engine = Engine()

if __name__ == "__main__":
    gtk.threads_init()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    ECEL_GUI(engine)
    gtk.main()
