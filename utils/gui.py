import gtk

def show_alert_message(parent_window, msg):
    alert = gtk.MessageDialog(parent_window, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
                              gtk.BUTTONS_CLOSE, msg)
    alert.run()
    alert.destroy()


def show_error_message(parent_window, msg):
    alert = gtk.MessageDialog(parent_window, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,
                              gtk.BUTTONS_CLOSE, msg)
    alert.run()
    alert.destroy()