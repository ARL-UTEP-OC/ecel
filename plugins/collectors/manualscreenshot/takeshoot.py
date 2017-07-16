import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk
import getpass
import os
import datetime
from time import sleep

import autopy


class CaptureScreen():

    def __init__(self):

        self.ip_entry_text = ""
        self.port_entry_text = ""
        self.initial_entry_text = ""
        self.comment_entry_text = ""

        response = self.save_shot()
        if response == Gtk.ResponseType.ACCEPT:
            # wait 1 second before taking the snapshot
            while Gdk.events_pending():
                Gtk.main_iteration()
            sleep(1)

            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            #take the snapshot
            bitmap = autopy.bitmap.capture_screen()
            savepath = os.path.join(os.getcwd(), 'plugins', 'collectors', 'manualscreenshot', 'raw')
            savefilename = self.comment_entry_text.strip().replace("-","") + "-" + timestamp
            savefull = os.path.join(savepath,savefilename+".png")
            bitmap.save(savefull) #TODO: Fix to have raw folder created!

            #write to metafile
            f = open(os.path.join(savepath,"."+savefilename), 'w')
            string = "[{\n" + \
                     " \"ip\" : \"" + self.ip_entry_text + "\"\n"\
                     " \"port\" : \"" + self.port_entry_text + "\"\n"\
                     " \"initial\" : \"" + self.initial_entry_text + "\"\n"\
                     " \"timestamp\" : \"" + timestamp + "\"\n"\
                     " \"savepath\" : \"" + savefull + "\"\n"\
                     " \"comment\" : \"" + self.comment_entry_text + "\"\n"\
                     "}]\n"
            f.write(string)
            f.close()
            #print "write metadata to:",os.path.join(savepath,"."+savefilename)
            #print "Screen shot taken:", savefull
        #else:
            #print "cancelled"

    def save_shot(self):
        # create a new window
        dialog = Gtk.Dialog("Manual ScreenShot",
                            None,
                            Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
                             Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))

        dialog.set_size_request(400, 250)
        dialog.set_title("Manual ScreenShot Comment ECEL V2.0")

        table = Gtk.Table(5,2,False)
        table.show()
        # create ip row
        ipLabel = Gtk.Label("IP")
        ipEntry = Gtk.Entry()
        table.attach(ipLabel, 0, 1, 0, 1)
        table.attach(ipEntry, 1, 2, 0, 1)
        ipLabel.show()
        ipEntry.show()

        # create Port row
        portLabel = Gtk.Label("Port")
        portEntry = Gtk.Entry()
        table.attach(portLabel, 0, 1, 1, 2)
        table.attach(portEntry, 1, 2, 1, 2)
        portLabel.show()
        portEntry.show()

        # create initial row
        initialLabel = Gtk.Label("Initials")
        initialEntry = Gtk.Entry()
        table.attach(initialLabel, 0, 1, 2, 3)
        table.attach(initialEntry, 1, 2, 2, 3)
        initialLabel.show()
        initialEntry.show()

        #create the comment entry field
        maxChar = 64
        commentEntry = Gtk.Entry()
        commentEntry.set_max_length(maxChar)
        commentEntry.insert_text("Enter Comment",0)
        commentEntry.select_region(0, len(commentEntry.get_text()))
        table.attach(commentEntry, 0, 2, 3, 4)
        commentEntry.show()

        dialog.vbox.pack_start(table,True,True,0)

        response = dialog.run()

        self.ip_entry_text = ipEntry.get_text()
        self.port_entry_text = portEntry.get_text()
        self.initial_entry_text = initialEntry.get_text()
        self.comment_entry_text = commentEntry.get_text()
        dialog.hide()
        dialog.destroy()
        return response