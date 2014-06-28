#!/usr/bin/env python
# coding:utf-8
# RPiCar trace sensor

from . import Sensor
from config import *

class Light(Sensor):
    def __init__(self, name = 'Light', weight = None):
        Sensor.__init__(self, name)
        return Sensor.set_vote(self, PIN_LEFT_LGT, PIN_RIGHT_LGT, weight = weight or -2)