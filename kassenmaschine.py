#!/usr/bin/env python3

from kassenmaschine import KassenMaschine

if __name__ == "__main__":

    km = KassenMaschine()

    #this will block
    km.worker()
