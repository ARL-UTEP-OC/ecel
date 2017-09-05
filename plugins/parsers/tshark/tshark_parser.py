import os
import subprocess
import gobject
from engine.parser import Parser
import fcntl

class TSharkParser(Parser):
    type = "parsers.TShark"

    def __init__(self, collector):
        super(TSharkParser, self).__init__(collector)
        if os.name == 'nt':
            self.script_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tshark_parser.bat")
        else:
            self.script_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tshark_parser.sh")

    def parse(self):
        if os.name == 'nt':
            subprocess.Popen(
                [self.script_file, self.file_or_dir, self.parsed_folder],
                cwd=os.path.dirname(os.path.realpath(__file__)),
                stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
        else:
            subprocess.call([self.script_file, self.file_or_dir, self.parsed_folder], shell=False)

    def parse(self, text_buffer):
        self.text_buffer = text_buffer
        if os.name == 'nt':
            subprocess.Popen(
                [self.script_file, self.file_or_dir, self.parsed_folder],
                cwd=os.path.dirname(os.path.realpath(__file__)),
                stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
        else:
            self.sub_proc = subprocess.Popen([self.script_file, self.file_or_dir, self.parsed_folder], stdout=subprocess.PIPE, shell=False)
            gobject.timeout_add(100, self.update_textbuffer)

    def non_block_read(self, output):
        ''' even in a thread, a normal read with block until the buffer is full '''
        fd = output.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        try:
            return output.read()
        except:
            return ''

    def update_textbuffer(self):
        self.text_buffer.insert_at_cursor(self.non_block_read(self.sub_proc.stdout))
        res = self.sub_proc.poll() is None
        if res == False:
            self.text_buffer.insert_at_cursor("Processing Completed")
        return res
