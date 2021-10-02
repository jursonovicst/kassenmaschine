import sys

class CDisplay:

    def __init__(self, nrow=4, welcome=''):
        self._rows = []
        for i in range(nrow):
            self._rows.append("")
        self._nrow = nrow

        #start fresh
        self.clearscreen()

    def refresh(self):

        self.clearscreen()

        for row in self._rows:
            print(row)

    def setrow(self, string, nrow):
        assert nrow<self._nrow, "row '"+nrow+"' does not exist!"

        self._rows[nrow] = string.strip()

    def clearscreen(self):
        #clear terminal
        sys.stdout.write(chr(27) + "[2J")