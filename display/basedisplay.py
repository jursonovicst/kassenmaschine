from threading import Timer


class BaseDisplay:

    def __init__(self, nrow=4, refresh=0.5, welcome=''):
        assert nrow > 0, "Number of rows must be greater than 0, received: '%d'" % nrow
        self._nrow = nrow

        # create a buffer
        self._rows = []
        for i in range(nrow):
            self._rows.append('')

        # clean and print welcome message
        self.cls()

        if welcome:
            self.prt(welcome, 0)

        self.__timer(refresh)

    def __timer(self, refresh):
        timer = Timer(refresh, self.__timer, args=[refresh])
        timer.start()

        self.rfr()

    def rfr(self):
        pass

    def prt(self, string: str, row: int):
        assert 0 <= row < self._nrow, f"Wrong row index: '{row}'!"

        # update buffer
        self._rows[row] = string[:20] if len(string) > 20 else f"{string:20s}"

    def cls(self):
        for i in range(self._nrow):
            self.prt('', i)

    def cln(self, no):
        self.prt('', no)
