#!/usr/bin/env python

# example progressbar.py

import pygtk

pygtk.require('2.0')
import gtk

class ProgressBar(gtk.Window):

    # Clean up allocated memory and remove the timer
    def destroy_progress(self, widget, data=None):
        self.destroy()

    # Update the value of the progress bar so that we get
    # some movement
    def setValue(self, pvalue):
        # Set the new value
        self.pbar.set_fraction(pvalue)

    def __init__(self):
        super(ProgressBar, self).__init__()

        #Configure the Window
        self.set_resizable(False)
        self.connect("destroy", self.destroy_progress)
        self.set_title("Progress Bar")
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_size_request(460, 50)
        self.set_border_width(0)

        #Create the VBox in case we want to add additional items later
        vbox = gtk.VBox(False, 5)
        vbox.set_border_width(10)
        self.add(vbox)
        vbox.show()

        # Create the ProgressBar
        self.pbar = gtk.ProgressBar()
        self.pbar.set_fraction(0.0)
        self.pbar.set_text("Starting")
        vbox.add(self.pbar)
        self.pbar.show()

        #Display the Window
        self.show()
