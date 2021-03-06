#!/usr/bin/env python3

""" a slot machine game
"""

from random import randint
from time import sleep
from utils import Loop, range1, first, sjoin, nl

num_reels  = 3
pause_time = 0.05
first_stop = 30     # stop first reel
reel_delay = 25     # range of delay to stop each reel
winmsg     = "You've won!! Collect your prize : %d"

symbols = {
    '❄': 100,
    '⌘': 200,
    '✿': 500,
    '❖': 1000,
    '✬': 2500,
 }


class Reel(object):
    def __init__(self, rotations, max_cycle):
        self.reel      = Loop(symbols.keys(), name="symbol")
        self.rotations = rotations
        self.max_cycle = max_cycle

    def symbol(self, cycle=0):
        if cycle and cycle <= self.max_cycle:
            self.rotate()
        return self.reel.symbol

    def rotate(self): self.reel.next(self.rotations)


class SlotMachine(object):
    def run(self, pause_time, display=True):
        """Run the machine, return tuple of (symbol line, win_amount)."""

        rotations    = [randint(1,4) for _ in range(num_reels)]    # reel rotations per cycle
        rd           = reel_delay
        total_cycles = [randint(x, x+rd) for x in range(first_stop, first_stop + rd*num_reels, rd)]

        reels        = [Reel(rotations, max_cycle) for rotations, max_cycle in zip(rotations, total_cycles)]

        for cycle in range1(max(total_cycles)):
            line = sjoin( [reel.symbol(cycle) for reel in reels] )
            if display: print(nl*5, line)
            sleep(pause_time)

        return self.done(reels, display, line)

    def done(self, reels, display, line):
        S      = [r.symbol() for r in reels]
        won    = bool(len(set(S)) == 1)
        amount = symbols[first(S)] if won else 0

        if won and display:
            print(winmsg % symbols[first(S)])
        return line, amount


def test():
    slots   = SlotMachine()
    runs    = [slots.run(0, False) for _ in range(300)]
    wins    = len([r for r in runs if r[1]])
    total   = sum(r[1] for r in runs)
    showall = False

    for run in runs:
        if showall or run[1]:
            print("%8s %6s" % run, nl)
    print(" wins", wins)
    print(" total", total)


if __name__ == "__main__":
    SlotMachine().run(pause_time)
    # test()
