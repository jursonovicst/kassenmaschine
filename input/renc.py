from threading import Lock
import RPi.GPIO as GPIO
import Queue


class REnc:

    def __init__(self, name, pin_a, pin_b, eventqueue):

        self._name = name
        self._pin_a = pin_a
        self._pin_b = pin_b
        self._eventqueue = eventqueue

        self._lock = Lock()

        GPIO.setwarnings(True)
        GPIO.setmode(GPIO.BCM)  # Use BOARD mode

        # define the Encoder switch inputs
        GPIO.setup(self._pin_a, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self._pin_b, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # setup callback thread for the A and B encoder
        # use interrupts for all inputs
        GPIO.add_event_detect(self._pin_a, GPIO.RISING, callback=self.__interrupt)  # NO bouncetime
        GPIO.add_event_detect(self._pin_b, GPIO.RISING, callback=self.__interrupt)  # NO bouncetime

        # assume initial state
        self._state_a = 1
        self._state_b = 1

    def __interrupt(self, pin):

        # read both of the switches
        state_a = GPIO.input(self._pin_a)
        state_b = GPIO.input(self._pin_b)

        # now check if state of A or B has changed
        # if not that means that bouncing caused it
        if state_a == self._state_a and state_b == self._state_b:  # Same interrupt as before (Bouncing)?
            return  # ignore interrupt!

        if state_a and state_b:  # Both one active? Yes -> end of sequence
            self._lock.acquire()  # get lock
            try:
                if pin == self._pin_a:  # Turning direction depends on
                    self._eventqueue.put_nowait("%s-UP" % self._name)
                else:  # so depending on direction either
                    self._eventqueue.put_nowait("%s-DOWN" % self._name)
            except Queue.Full:
                pass
            self._lock.release()  # and release lock

        # remember states
        self._state_a = state_a  # remember new state
        self._state_b = state_b  # remember new state
