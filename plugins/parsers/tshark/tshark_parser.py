import os
import subprocess
import gobject
from engine.parser import Parser
import fcntl
import definitions

class TSharkParser(Parser):
    type = "parsers.TShark"

    def __init__(self, collector):
        super(TSharkParser, self).__init__(collector)
        if os.name == 'nt':
            self.script_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tshark_parser.bat")
        else:
            self.script_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tshark_parser.sh")
        self.parserInputs = [self.script_file, self.file_or_dir, self.parsed_folder,definitions.ECEL_PARSER_ROOT]


