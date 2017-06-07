from engine.collector import ManualCollector
from plugins.collectors.manualscreenshot import takeshoot

class manualscreenshot(ManualCollector):
    command = "python takeshoot.py"

    def __init__(self, collector_config):
        super(manualscreenshot, self).__init__(collector_config)

        self.command_description = "Take Screenshot"

    def build_commands(self):
        self.commands.append(self.command)

    def run(self):
        takeshoot.CaptureScreen()