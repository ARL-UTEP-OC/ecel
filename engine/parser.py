import os
import subprocess
import re
import gobject
import fcntl

class MetadataPostCondition(object):
    def assert_true(self):
        return True


class RegexPostCondition(object):
    def __init__(self, file_re):
        self.file_re = file_re

    def assert_true(self, file):
        return re.match(self.file_re, file)


class Parser(object):

    def __init__(self, collector):
        self.post_conditions = []
        self.collector = collector
        self.file_or_dir = collector.output_dir
        self.parsed_folder = os.path.join(collector.base_dir, "parsed")
        self.parserInputs = []
        self.status = "pending"

    def parse(self):
        if (os.path.isdir(self.file_or_dir)):
            self.__parse_directory(self.file_or_dir)
        else:
            self.__parse_file(self.file_or_dir)

    def parse(self, text_buffer):
        self.text_buffer = text_buffer
        if os.name == 'nt':
            subprocess.Popen(
                self.parserInputs,
                cwd=os.path.dirname(os.path.realpath(__file__)),
                stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
            self.status = "running"
        else:
            self.sub_proc = subprocess.Popen(self.parserInputs, stdout=subprocess.PIPE, shell=False)
            self.status = "running"
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
            self.status = "complete"
            self.text_buffer.insert_at_cursor("Finished. Please close this window.")
        return res
####


    def do_file(self, file_path):
        print ""

    def __parse_file(self, file_path):
        if self.__meets_post_conditions(file_path):
            self.do_file(file_path)

    def __parse_directory(self, dir):
        for file in os.listdir(dir):
            self.__parse_file(os.path.join(dir, file))

    def __meets_post_conditions(self, file_path):
        for post_condition in self.post_conditions:
            if not post_condition.assert_true(file_path):
                return False
        return True

    def dump_to_file(self, lines):
        with open(self.pfolder, 'w') as outfile:
            outfile.writelines(lines)
