import logging
import time

import numpy as np
import pandas as pd
from multiprocessing import Queue
from display import Display
from input import REnc, Swi, PoS, Keyboard


class KassenMaschine:
    def __init__(self):
        # create event queue
        self._events = Queue(5)

        # init display
        self._display = Display(nrow=4, welcome="Oli's Kassenmaschine")

        # init keyboard input collection
        self._keyboard = Keyboard(self._events)

        # init rotary encoders
        self._renc_discount = REnc('DISC', 5, 6, self._events)
        self._swi_discount = Swi('ZERODISC', 13, self._events)
        self._discount = 0

        self._renc_bias = REnc('BIAS', 17, 27, self._events)
        self._swi_bias = Swi('ZEROBIAS', 22, self._events)
        self._bias = 0

        # init switches
        self._swi_substract = Swi('SUBS', 26)
        self._swi_reset = Swi('RESET', 19, self._events)

        # init POS terminal
        self._pos = PoS('POS', self._events)

        # init data structure
        dtypes = np.dtype([
            ('Produkt', str),
            ('Preis', float),
        ])
        data = np.empty(0, dtype=dtypes)
        self._basket = pd.DataFrame(data)

    def _addproduct(self, produkt):
        if self._swi_substract.ishigh():
            self._basket = self._basket.append({'Produkt': produkt, 'Preis': float(produkt[-3:]) / 100},
                                               ignore_index=True)
        else:
            match = self._basket.index[self._basket.Produkt == produkt].tolist()
            if match:
                self._basket.drop(match[0], inplace=True)

    def _update(self):
        i = 0
        for index, row in self._basket.tail(3).iterrows():
            self._display.prt("%-14s %3.2fE" % (row['Produkt'][:13], row['Preis']), i)
            i += 1
        summary = self._basket['Preis'].sum()
        self._display.prt("TOT: (%2d%%) %8.2fE " % (self._discount * 100, summary * (1 - self._discount) + self._bias),
                          3)

        # clear empty lines, if any
        if self._basket.shape[0] < 3:
            self._display.cln(2)

        if self._basket.shape[0] < 2:
            self._display.cln(1)

        if self._basket.shape[0] < 1:
            self._display.cln(0)

    def _pay(self, id: str, payment: float, balance: float):
        #                   12345678901234567890
        self._display.prt(f"Credit card {id}", 0)
        self._display.prt(f" payment: {payment:5.2f}E", 1)
        self._display.prt(f" balance: {balance:5.2f}E", 2)
        self._display.prt(f"*** Thank you! ***", 3)

    def _reset(self):
        self._basket.drop(self._basket.index, inplace=True)
        self._discount = 0
        self._bias = 0

    def worker(self):
        try:
            while True:

                event = self._events.get()
                assert type(event) is str, "I expect str, but got '%s'" % type(event)

                print("<-- %s" % event)

                if event.startswith('ZOE-'):
                    if event == 'ZOE-RESET':
                        self._reset()
                    elif event == 'ZOE-0RABATT':
                        self._discount = 0
                    elif event == 'ZOE-10RABATT':
                        self._discount = 0.1
                    elif event == 'ZOE-20RABATT':
                        self._discount = 0.2
                    elif event == 'ZOE-30RABATT':
                        self._discount = 0.3
                    self._update()

                elif event.startswith('DISC-'):
                    if event == 'DISC-UP':
                        if self._discount < 0.99:
                            self._discount += 0.01
                    elif event == 'DISC-DOWN':
                        if self._discount > 0:
                            self._discount -= 0.01
                    self._update()

                elif event.startswith('ZERODISC-'):
                    if event == 'ZERODISC-FALL':
                        self._discount = 0
                    self._update()

                elif event.startswith('BIAS-'):
                    if event == 'BIAS-UP':
                        if self._bias < 100:
                            self._bias += 0.33333333
                    elif event == 'BIAS-DOWN':
                        if self._bias > -100:
                            self._bias -= 0.33333333
                    self._update()

                elif event.startswith('ZEROBIAS-'):
                    if event == 'ZEROBIAS-FALL':
                        self._bias = 0
                    self._update()

                elif event.startswith('RESET-'):
                    if event == 'RESET-FALL':
                        # reset content
                        self._reset()
                    self._update()

                elif event == 'POS':
                    # customer want's to pay, then pay
                    try:
                        balance = float(self._pos.balance)
                    except ValueError:
                        raise ValueError(f"Something went wrong, RFID text is not numeric: '{self._pos.balance}'")

                    payment = self._basket['Preis'].sum() * (1 - self._discount) + self._bias
                    balance -= payment
                    self._pos.balance = balance

                    # display payment confirmation
                    self._pay(self._pos.id, payment, balance)

                elif event[-3:].isdigit():
                    self._addproduct(event)
                    self._update()

        except KeyboardInterrupt:
            self._keyboard.stop()

            # wait for pos
            self._pos.join(2)
