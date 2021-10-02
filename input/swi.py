import RPi.GPIO as GPIO


class Swi:

    def __init__(self, name, pin, eventqueue=None):

        self._name = name
        self._pin = pin
        self._eventqueue = eventqueue

        GPIO.setwarnings(True)
        GPIO.setmode(GPIO.BCM)  # Use BOARD mode

        # define the switch inputs
        GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self._state = self.state

        # setup callback thread for rising and falling events
        # use interrupts
        if self._eventqueue is not None:
            GPIO.add_event_detect(self._pin, GPIO.BOTH, callback=self.__interrupt)  # NO bouncetime

    def __interrupt(self, pin):
        if self._state == GPIO.HIGH and self.state == GPIO.LOW:
            self._eventqueue.put_nowait("%s-FALL" % self._name)
        elif self._state == GPIO.LOW and self.state == GPIO.HIGH:
            self._eventqueue.put_nowait("%s-RISE" % self._name)

        self._state = self.state

    @property
    def state(self):
        return GPIO.input(self._pin)

    def ishigh(self):
        return self.state == GPIO.HIGH

    def islow(self):
        return self.state == GPIO.LOW
