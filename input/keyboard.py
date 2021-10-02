import threading
import sys
import select
from multiprocessing import Event


class Keyboard:

    def __init__(self, eventqueue):
        # assert isinstance(eventqueue, Queue), "Expect multiprocessing.Queue, got '%s'" % type(eventqueue)

        self._stop = Event()
        self._thread = threading.Thread(target=Keyboard._worker, args=(eventqueue, self._stop,))
        self._thread.start()

    def stop(self):
        self._stop.set()
        self._thread.join(1)

    @classmethod
    def _worker(cls, eventqueue, stop):
        while not stop.is_set():
            if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
                line = sys.stdin.readline()
                if line:
                    eventqueue.put(line.strip())
                else:  # an empty line means stdin has been closed
                    stop.set()
