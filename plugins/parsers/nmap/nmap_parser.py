import os
import subprocess
import definitions
from engine.parser import Parser

class NMapParser(Parser):
    type = "parsers.NMap"

    def __init__(self, collector):
        super(NMapParser, self).__init__(collector)
        if os.name == 'nt':
            self.script_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "nmap_parser.bat")
        else:
            self.script_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "nmap_parser.sh")

    def parse(self):
        if os.name == 'nt':
            subprocess.Popen(
                [self.script_file, self.file_or_dir, self.parsed_folder],
                cwd=os.path.dirname(os.path.realpath(__file__)),
                stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
        else:
            subprocess.call([self.script_file, self.file_or_dir, self.parsed_folder], shell=False)