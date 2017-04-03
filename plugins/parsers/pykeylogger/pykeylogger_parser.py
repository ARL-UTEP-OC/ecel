import os
import subprocess

from core.parser import Parser


class PyKeyloggerParser(Parser):

    def __init__(self, plugin):
        super(PyKeyloggerParser, self).__init__(plugin)
        self.click_dir = os.path.join(self.file_or_dir, "click_images")
        self.timed_dir = os.path.join(self.file_or_dir, "timed_screenshots")
        self.file_or_dir = os.path.join(self.file_or_dir, "detailed_log", "logfile.txt")
        if os.name == 'nt':
            self.script_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "keylogger_parser.bat")
        else:
            self.script_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "keylogger_parser.sh")

    def parse(self):
        if os.name == 'nt':
            subprocess.Popen(
                [self.script_file, self.file_or_dir, self.parsed_folder, self.click_dir, self.timed_dir], cwd=os.path.dirname(os.path.realpath(__file__)),
                stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
        else:
            subprocess.Popen([self.script_file, self.file_or_dir, self.parsed_folder, self.click_dir, self.timed_dir], shell=False)
