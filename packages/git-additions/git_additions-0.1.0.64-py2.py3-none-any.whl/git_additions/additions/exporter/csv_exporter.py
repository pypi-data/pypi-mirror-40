import csv

import os


class CSVExporter(object):

    def __init__(self):
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)

    def set_lines(self, lines):
        self.lines = lines

    def write_content(self, file_path):
        if not file_path.startswith('/'):
            file_path = '%s/%s' % (os.getcwd(), file_path)
        with open(file_path, 'w+') as csv_file:
            wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            for line in self.lines:
                wr.writerow(line)
