import os
import subprocess

from engine.parser import Parser

class NMapParser(Parser):
    type = "parsers.Nmap"

    def __init__(self, collector):
        super(NMapParser, self).__init__(collector)

