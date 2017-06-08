from engine.collector import AutomaticCollector

class pykeylogger(AutomaticCollector):
    def build_commands(self):
        self.commands.append("python keylogger.pyw")