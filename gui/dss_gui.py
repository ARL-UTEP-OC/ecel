import gtk
import os
import glob
import time
import definitions
import utils.gui
import utils.helpers
from engine.engine import Engine as app_engine
from datetime import datetime, timedelta

#gui to choose analysis time frame window
#once timeframe is selected extract network data from pcap files
#send extracted data to ecel-model module

class DssGUI(gtk.Window):
    def __init__(self, parent, collectors):
        super(DssGUI, self).__init__()

        self.main_gui = parent
        
        self.collectors = collectors
        self.set_title("DSS")
        self.set_modal(True)
        self.set_transient_for(self.main_gui)
        self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.set_size_request(275, 250)
        self.set_resizable(False)
        
        #create combobox with timeframe options
        self.time_options = gtk.ListStore(str)
        self.options_list = ["Select a timeframe", "5 minutes", "30 minutes", "1 hour", "All"]
        for i in xrange(len(self.options_list)):
            self.time_options.append([self.options_list[i]])
        
        self.timeframe_combobox = gtk.ComboBox(self.time_options)
        self.timeframe_combobox.set_active(0)
        
        cell = gtk.CellRendererText()
        self.timeframe_combobox.pack_start(cell,True)
        self.timeframe_combobox.add_attribute(cell, "text", 0)
        
        #create buttons
        button_analyze = gtk.Button("Analyze")
        button_analyze.connect("clicked", self.analyze)
        button_cancel = gtk.Button("Cancel")
        button_cancel.connect("clicked", self.close_dialog)
        
        #create labels for title and error
        title = gtk.Label("Select Timeframe to Analyze:")
        self.errormsg = gtk.Label()
        
        #pack layout
        vbox = gtk.VBox()
        vbox.pack_start(title)
        vbox.pack_start(self.errormsg)
        vbox.pack_start(self.timeframe_combobox)
        
        hbox_okcancel = gtk.HBox()
        hbox_okcancel.pack_start(button_cancel,True,True, 5)
        hbox_okcancel.pack_start(button_analyze,True,True, 5)
        vbox.pack_start(hbox_okcancel,False, False, 10)

        self.add(vbox)
        self.show_all()

    def close_dialog(self, event):
        self.hide_all()
        
    def analyze(self,event):
        self.errormsg.set_text("")
        selected = self.timeframe_combobox.get_active_text()
        if selected == "Select a timeframe" or selected not in self.options_list:
            self.errormsg.set_text("Invalid timeframe option")
            return

        #merge and extract desired timeframe from all pcaps
        pcap_dir = self.mergePcaps()
        self.timeFilterPcap(selected, pcap_dir)
        
        self.cleanup(pcap_dir)
        
        
    # merge all pcaps in directory into one single pcap named dss_merged_output.pcap
    # returns directory where tshark plugin stores raw pcaps
    def mergePcaps(self):
        #check tshark plugin exists
        pcap_dir = ""
        tshark_found = False
        for c in self.collectors:
            if c.name == "tshark":
                tshark_found = True
                pcap_dir = c.output_dir
                
        if not tshark_found:
            self.errormsg.set_text("Error: tshark plugin not found")
            return
            
        #check for pcap files in tshark plugins folder
        pcap_file_list = glob.glob(pcap_dir+'/*.pcap*')
        if not pcap_file_list:
            self.errormsg.set_text("No PCAPS in directory:\n%s" % pcap_dir)
            return
        
        #use mergecap to merge all pcaps in pcap_dir
        pcap_file_string = " ".join(pcap_file_list)
        cmd = "mergecap -w "+pcap_dir+"/dss_merged_output.pcap "+pcap_file_string
        utils.helpers.execCommand(cmd)
        
        return pcap_dir
    
    #execute system command to call tshark to filter merged pcap and output to new file
    # pcap_dir : root directory of raw pcap files without trailing /
    # time_filter : timestamp in the form 2018-02-14 17:13:48.342691
    def timeFilterPcap(self, selected, pcap_dir):
        
        #filter packets by selected timeframe and output to new file
        if selected == "5 minutes":
            timeDelta = timedelta(minutes=-5)
        elif selected == "30 minutes":
            timeDelta = timedelta(minutes=-30)
        elif selected == "1 hour":
            timeDelta = timedelta(hours=-1)
        elif selected == "All":
            timeDelta = timedelta(weeks =-5200)#back 100 years
        else:
            self.errormsg.set_text("Invalid timeframe option")
            return
        
        timeFilter = datetime.now() + timeDelta # timestamp in the form : 2018-02-14 17:13:48.342691
        
        if not os.path.isfile(pcap_dir+"/dss_merged_output.pcap"):
            self.errormsg.set_text("Error: merged output file not found")
            return
        
        #use tshark to filter merged pcap by time
        cmd = "tshark -Y 'frame.time >= \""+str(timeFilter)+"\"' -r "+pcap_dir+"/dss_merged_output.pcap -w "+pcap_dir+"/dss_merged_time_filtered_output.pcap"
        utils.helpers.execCommand(cmd)
        
        #call ecel-model to get suggestions
        #model must already exist in DB and mongod must be running
        
        #TODO CHECK THAT MONGOD IS RUNNING AND DB EXISTS
        cmd = definitions.ECEL_DSS_ROOT+"run.sh -i "+pcap_dir+"/dss_merged_time_filtered_output.pcap -d "+definitions.ECEL_DSS_ROOT
        
        utils.helpers.execCommand(cmd)

    #remove files generated in analyze function
    def cleanup(self, pcap_dir):
        try:
            os.remove(pcap_dir+"/dss_merged_output.pcap")
            os.remove(pcap_dir+"/dss_merged_time_filtered_output.pcap")
        
        except OSError as err:
            print "System Error:", err
