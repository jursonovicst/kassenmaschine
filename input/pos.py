from threading import Thread
from multiprocessing import Queue
from mymfrc522 import MyMFRC522
import time
import logging
import RPi.GPIO as GPIO


class PoS(Thread):
    def __init__(self, name: str, eventqueue: Queue):
        super().__init__(name=name)
        self._eventqueue = eventqueue
        self._reader = MyMFRC522(pin_rst=25, pin_mode=GPIO.BCM)

        self._id = None
        self._balance = 0

        self.start()

    @property
    def id(self) -> str:
        return self._id

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, val):
        self._reader.write(f"{float(val):.2f}")

    def run(self) -> None:
        lastid = None
        lastseen = None
        while True:
            try:
                # read with no block
                id, text = self._reader.read_no_block()

                # check, if read successful AND first read, or new id, or id after 5 sec
                if id is not None and (lastid is None or lastid != id or time.time() - lastseen > 5):
                    self._id = id
                    self._balance = float(text)

                    self._eventqueue.put_nowait(f"{self.name}")

                    lastid = id
                    lastseen = time.time()
            except KeyboardInterrupt:
                break
            except ValueError:
                logging.warning(f"Card {id} has not been formatted: '{text}'")
                pass
            except Queue.Full:
                pass

            time.sleep(0.1)
