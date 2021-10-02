from basedisplay import BaseDisplay
from .RPi_I2C_driver import lcd
from threading import Lock


class LCD2004(BaseDisplay):

    def __init__(self, nrow=4, refresh=0.5, welcome=''):
        self._lcd = lcd()
        self._lock = Lock()

        BaseDisplay.__init__(self, nrow, refresh, welcome)

    def rfr(self):
        """
        Refresh screen
        """
        if self._lock.acquire(False):
            for i in range(self._nrow):
                self._lcd.lcd_display_string(self._rows[i], i + 1)
            self._lock.release()

    def cls(self):
        """
        Clear screen
        """
        BaseDisplay.cls(self)

        self._lock.acquire()
        self._lcd.lcd_clear()
        self._lock.release()

    def cln(self, no):
        """
        Clear line
        :param no: line number
        """
        self.prt('                    ', no)
