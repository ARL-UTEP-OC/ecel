#!/usr/bin/env python

# example progressbar.py

import pygtk

pygtk.require('2.0')
import gtk
import fcntl
import gobject

class ProgressBarDetails(gtk.Window):

    # Clean up allocated memory and remove the timer
    def destroy_progress(self, widget, data=None):
        self.destroy()

    # Update the value of the progress bar so that we get
    # some movement
    def setValue(self, pvalue):
        # Set the new value
        self.pbar.set_fraction(pvalue)

    def appendText(self, text):
        if text.strip() != "":
            self.msg_i += 1
            i = self.text_buffer.get_end_iter()
            self.text_buffer.insert(i, str(text), -1)
            return True

    def __init__(self):
        super(ProgressBarDetails, self).__init__()

        #Configure the Window
        self.set_resizable(False)
        self.connect("destroy", self.destroy_progress)
        self.set_title("Progress Bar")
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_size_request(460, 150)
        self.set_border_width(0)

        #Create the VBox in case we want to add additional items later
        self.vbox = gtk.VBox(False, 5)
        self.vbox.set_border_width(10)
        self.add(self.vbox)
        self.vbox.show()

        #create the scrolled window
        self.scrolled_window =gtk.ScrolledWindow()
        self.scrolled_window.set_usize(460, 100)
        self.vbox.add(self.scrolled_window)
        self.scrolled_window.show()

        self.text_view = gtk.TextView()
        self.msg_i = 0
        self.text_buffer = self.text_view.get_buffer()
        self.scrolled_window.add_with_viewport(self.text_view)
        self.text_view.connect("size-allocate", self.autoscroll)
        self.text_view.show()

        # Create the ProgressBar
        self.pbar = gtk.ProgressBar()
        #self.pbar.set_usize(460, 40)
        self.pbar.set_fraction(0.0)
        self.vbox.add(self.pbar)
        self.pbar.show()

        #Display the Window
        self.show()

    def autoscroll(self, *args):
        """The actual scrolling method"""
        adj = self.scrolled_window.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())
