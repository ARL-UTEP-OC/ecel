from Config.Controller.EngineController import *
from Config.Controller.PluginController import *
from Config.View.Engine.MasterView import MakeMasterView
from Config.View.Plugin.MasterView import MakePluginsView
import gtk

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_FILE_NAME = 'config.json'


def scaffold_initial_files():
    EngineController(BASE_DIR, CONFIG_FILE_NAME)
    PluginsController(BASE_DIR, CONFIG_FILE_NAME)


def call_plugins_config(event):
    MakePluginsView(BASE_DIR, CONFIG_FILE_NAME)
    show_notice()

def call_engine_config(event):
    MakeMasterView(BASE_DIR, CONFIG_FILE_NAME)
    show_notice()

def show_notice():
    dialog = gtk.Dialog("Notice",
                        None,
                        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                        (gtk.STOCK_CLOSE, gtk.RESPONSE_ACCEPT))
    noticeLabel = gtk.Label("Restart ECEL for changes to take effect.")
    noticeLabel.show()
    dialog.vbox.pack_start(noticeLabel)
    dialog.run()
    dialog.hide_all()
    dialog.destroy()

if __name__ == "__main__":
    print "Configuration"

