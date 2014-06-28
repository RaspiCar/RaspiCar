#!/usr/bin/env python
# coding:utf-8
# RPiCar sensor prototype

from RPi import GPIO as io
import math
from threading import RLock

class Sensor(object):
    def __init__(self, name = None):
        self.name = name or self.__class__.__name__
        self._left_pin = None
        self._right_pin = None
        self._neutral_pin = None
        self._votes = [0, 0, 0]
        self._weight = 1
        self._request_vote = None
        self._last_vote_status = 0

    def add_vote_request(self, func):
        self._request_vote = func

    def vote_interrupt(self, pin):
        if pin == self._left_pin:
            idx = 0
        elif pin == self._neutral_pin:
            idx = 1
        elif pin == self._right_pin:
            idx = 2
        else:
            raise AttributeError(" [%s]vote interrupt can only be called by vote pin events." % self.name)
        self._votes[idx] = io.input(pin)
        if self._request_vote:
            self._request_vote(self._last_vote_status, self.vote_status())

    def vote_status(self):
        if not self._left_pin or not self._right_pin:
            raise ValueError(" [%s]vote requires at least left_pin and right_pin setted." % self.name)
        n = 1 - self._votes[1] * 0.5
        # needs to turn left : +, turn right : -
        ret =  self._weight * (self._votes[0] * n - self._votes[2] * n)
        self._last_vote_status = ret
        return ret

    def set_vote(self, lpin, rpin, npin = None, weight = 1, bouncetime = 50):
        if not lpin or not rpin:
            raise ValueError(" [%s]vote pins can't be set to none." % self.name)
        self._left_pin = lpin
        self._right_pin = rpin
        self._neutral_pin = npin
        self._weight = weight
        io.add_event_detect(lpin, edge = io.BOTH, callback = self.vote_interrupt, bouncetime = bouncetime)
        io.add_event_detect(rpin, edge = io.BOTH, callback = self.vote_interrupt, bouncetime = bouncetime)
        if npin:
            io.add_event_detect(npin, edge = io.BOTH, callback = self.vote_interrupt, bouncetime = bouncetime)


class SensorVote(object):
    def __init__(self, new_vote_callback = None):
        self._vote_poll = []
        self._last_vote_status = 0
        self._calc_vote_lock = RLock()
        self._new_vote = new_vote_callback

    def add_voter(self, sensor):
        if Sensor not in sensor.__class__.__bases__:
            raise TypeError(" sensor argument must be an instance of Sensor class.")
        self._vote_poll.append(sensor)
        sensor.add_vote_request(self.vote_fast)

    def remove_voter(self, sensor):
        if Sensor not in sensor.__class__.__bases__:
            raise TypeError(" sensor argument must be an instance of Sensor class.")
        del self._vote_poll[self._vote_poll.index(sensor)]

    def vote_fast(self, old, new):
        '''
        This is function usually called by interrupt
        '''
        self._calc_vote_lock.acquire()
        self._last_vote_status = self._last_vote_status - old + new
        self._calc_vote_lock.release()
        if self._new_vote:
            self._new_vote(self._last_vote_status)
        return self._last_vote_status

    def vote_full(self):
        '''
        This is function usually manully called
        '''
        rt = 0
        # raise caution if low priority sensors mostly(2/3) vote the opposite of higher ones
        caution = False
        self._calc_vote_lock.acquire()
        for s in self._vote_poll:
            _vt = s.vote_status()
            if not caution and math.copysign(1, rt) != math.copysign(1, _vt) and rt > _vt * 2 / 3.0:
                caution = True
            rt += _vt
        self._last_vote_status = rt
        self._calc_vote_lock.release()
        return rt, caution