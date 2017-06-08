from engine.collector import ManualCollector
from plugins.collectors.manualscreenshot import takeshoot
import os
import time

class manualscreenshot(ManualCollector):
    def __init__(self, collector_config):
        super(manualscreenshot, self).__init__(collector_config)

        self.command_description = "Take Screenshot"

    def build_commands(self):
        self.commands.append("python takeshoot.py")

    def run(self):
        #TODO: Need to fix the base collector class to not act like an automatic collector
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        #TODO: Order is wrong is collectors class. raw dir needs to be created first (maybe create in init)
        self.start_time = str(int(time.time()))
        self.create_metafile()

        takeshoot.CaptureScreen()