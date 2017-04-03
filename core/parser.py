import os
import re


class MetadataPostCondition(object):
    def assert_true(self):
        return True


class RegexPostCondition(object):
    def __init__(self, file_re):
        self.file_re = file_re

    def assert_true(self, file):
        return re.match(self.file_re, file)


class Parser(object):
    def __init__(self, plugin):
        self.post_conditions = []
        self.plugin = plugin
        self.file_or_dir = plugin.output_dir
        self.parsed_folder = os.path.join(plugin.base_dir, "parsed")
    def parse(self):
        if (os.path.isdir(self.file_or_dir)):
            self.__parse_directory(self.file_or_dir)
        else:
            self.__parse_file(self.file_or_dir)

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
