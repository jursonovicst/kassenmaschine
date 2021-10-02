from display import BaseDisplay
import sys


class Console(BaseDisplay):

    def __init__(self, nrow=4, refresh=0.4, welcome='', eventqueue=None):

        BaseDisplay.__init__(self, nrow, refresh, welcome, eventqueue)

    def prt(self, string, row):
        BaseDisplay.prt(self, string, row)

        # print
        sys.stdout.write(chr(27) + "[2J")
        for i in range(self._nrow):
            print(self._rows[i])

    def cls(self):
        sys.stdout.write(chr(27) + "[2J")

        # clean buffer
        for i in range(self._nrow):
            self._rows[i] = ''
