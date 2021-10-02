from console import CDisplay
import RPi_I2C_driver

class LDisplay(CDisplay):

    def __init__(self, nrow=4, welcome=''):
        CDisplay.__init__(self, nrow)
        self._lcd = RPi_I2C_driver.lcd()
        self._lcd.lcd_display_string(welcome, 1)
        for i in range(1,nrow+1):
            self._lcd.lcd_display_string('', i)


    def refresh(self):
        for i, row in enumerate(self._rows):
            self._lcd.lcd_display_string(row, i+1)

    def clearscreen(self):
        pass