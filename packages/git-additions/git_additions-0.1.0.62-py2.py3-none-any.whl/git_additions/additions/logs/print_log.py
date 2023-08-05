from __future__ import print_function

from git_additions.additions.logs.t_colors import TColors


class PrintLog(object):

    def __init__(self, lines):
        self.lines = lines

    def run(self):
        for line in self.lines:
            colors = TColors.COLORS
            colors.update({'line': line})
            log_line = \
                '{default}{line[0]} {green}{line[3]} {white}{line[1]}{yellow} [{line[2]}]  {darkgray}{line[4]}{default}'
            print(log_line.format(**colors))
