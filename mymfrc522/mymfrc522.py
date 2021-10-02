from mfrc522 import SimpleMFRC522, MFRC522
import RPi.GPIO as GPIO


class MyMFRC522(SimpleMFRC522):

    def __init__(self, pin_rst, pin_mode=GPIO.BCM):
        self.READER = MFRC522(pin_rst=pin_rst, pin_mode=pin_mode)
