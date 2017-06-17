import gtk
import signal
from engine.engine import Engine
from gui.main_gui import MainGUI

engine = Engine()

if __name__ == "__main__":
    gtk.threads_init()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    MainGUI(engine)
    gtk.main()