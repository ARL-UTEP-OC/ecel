import gtk
import signal
from engine.engine import Engine
from gui.ecel_gui import EcelGUI

engine = Engine()

if __name__ == "__main__":
    gtk.threads_init()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    EcelGUI(engine)
    gtk.main()
