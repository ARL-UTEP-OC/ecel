from engine.collector import AutomaticCollector

class pykeylogger(AutomaticCollector):
    command = "python keylogger.pyw"

    def build_commands(self):
        self.commands.append(self.command)