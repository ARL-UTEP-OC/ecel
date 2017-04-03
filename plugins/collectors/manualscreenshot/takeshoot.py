import getpass
import gtk
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
        if response == gtk.RESPONSE_ACCEPT:
            # wait 1 second before taking the snapshot
            while gtk.events_pending():
                gtk.main_iteration()
            sleep(1)

            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            #take the snapshot
            bitmap = autopy.bitmap.capture_screen()
            savepath = os.path.join(os.getcwd(), 'plugins', 'collectors', 'manualscreenshot', 'raw')
            savefilename = self.comment_entry_text.strip().replace("-","") + "-" + timestamp
            savefull = os.path.join(savepath,savefilename+".png")
            bitmap.save(savefull)

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
            print "write metadata to:",os.path.join(savepath,"."+savefilename)
            print "Screen shot taken:", savefull
        else:
            print "cancelled"

    def save_shot(self):
        # create a new window
        dialog = gtk.Dialog("My dialog",
                            None,
                            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                             gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

        dialog.set_size_request(400, 250)
        dialog.set_title("Manual ScreenShot Comment ECEL V2.0")

        table = gtk.Table(5,2,False)
        table.show()
        # create ip row
        ipLabel = gtk.Label("IP")
        ipEntry = gtk.Entry()
        table.attach(ipLabel, 0, 1, 0, 1)
        table.attach(ipEntry, 1, 2, 0, 1)
        ipLabel.show()
        ipEntry.show()

        # create Port row
        portLabel = gtk.Label("Port")
        portEntry = gtk.Entry()
        table.attach(portLabel, 0, 1, 1, 2)
        table.attach(portEntry, 1, 2, 1, 2)
        portLabel.show()
        portEntry.show()

        # create initial row
        initialLabel = gtk.Label("Initials")
        initialEntry = gtk.Entry()
        table.attach(initialLabel, 0, 1, 2, 3)
        table.attach(initialEntry, 1, 2, 2, 3)
        initialLabel.show()
        initialEntry.show()

        maxChar = 64
        # print str(maxChar) + " is the max length"
        commentEntry = gtk.Entry()
        commentEntry.set_max_length(maxChar)
        commentEntry.insert_text("Enter Comment")
        commentEntry.select_region(0, len(commentEntry.get_text()))
        table.attach(commentEntry, 0, 2, 3, 4)
        commentEntry.show()

        dialog.vbox.pack_start(table)

        response = dialog.run()

        self.ip_entry_text = ipEntry.get_text()
        self.port_entry_text = portEntry.get_text()
        self.initial_entry_text = initialEntry.get_text()
        self.comment_entry_text = commentEntry.get_text()
        dialog.hide_all()
        dialog.destroy()
        return response