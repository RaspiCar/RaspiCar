#!/usr/bin/env python
# coding:utf-8
# RPiCar trace sensor

from . import Sensor
from config import *

class Tracer(Sensor):
    def __init__(self, name = 'Tracer', weight = None):
        Sensor.__init__(self, name)
        Sensor.set_vote(self, PIN_LEFT_TRACER, PIN_RIGHT_TRACER, npin = PIN_MID_TRACER, weight = weight or 1)