#!/usr/bin/env python
# coding:utf-8
# RPiCar trace sensor

from . import Sensor
from config import *

class HumanOverride(Sensor):
    def __init__(self, name = 'Override', weight = None):
        Sensor.__init__(self, name)
        self.weight = weight or 4

    def do_override(self, inp):
        if inp == 'l':
            self._votes[0] = self.weight
            self._votes[1] = 0 
        elif inp == 'r':
            self._votes[1] = 1
            self._votes[1] = self.weight
        else:
            self._votes = [0, 0, 0]

    def vote_status(self):
        return sum(self._votes)
        