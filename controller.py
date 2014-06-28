#!/usr/bin/env python
# coding:utf-8
# RPiCar controller
from __future__ import print_function
from RPi import GPIO as io
import time
from datetime import datetime
from threading import Thread
from Queue import Queue, Empty
from config import *
import sys
from motor import motor
from speed import speed
from Sensor import SensorVote, Tracer, Light, HumanOverride

def setup():
    io.setmode(GPIO_MODE)

    io.setup(PIN_LEFT_TRACER, io.IN)
    io.setup(PIN_MID_TRACER, io.IN)
    io.setup(PIN_RIGHT_TRACER, io.IN)

    io.setup(PIN_LEFT_LGT, io.IN)
    io.setup(PIN_RIGHT_LGT, io.IN)

def cleanup(*args):
    for c in args:
        c.cleanup()
    io.cleanup()

def direction(motor, vote):
    if vote == 0:
        motor.go()
    elif vote < 0 :
        motor.turn_left(fast = int(vote) == vote)# fat = without neutral vote
    else:
        motor.turn_right(fast = int(vote) == vote)



class logger(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.q = Queue()

    def run(self):
        while self.q != None:
            try:
                print(self.q.get(False))
            except Empty:
                time.sleep(0.5)
    #print('%s%s%s%s' % (datetime.now().strftime('%X'), string, ' ' * (TERM_SIZE[0] - 8 - len(string)),  '\b' * TERM_SIZE[0]), end = '')

def main():
    from threading import Thread
    _logger = logger()
    def log(string):
        if _logger.q:
            _logger.q.put('%s%s' % (datetime.now().strftime('%X'), string))
    _logger.start()
    setup()
    m = motor()
    sv = SensorVote(new_vote_callback = lambda x:direction(m, x) or log('[NEW-VOTE] %s' % x))
    #t = Tracer.Tracer()
    #sv.add_voter(t)
    l = Light.Light()
    sv.add_voter(l)
    h = HumanOverride.HumanOverride()
    sv.add_voter(h)

    spd = speed()
    spd.start_monitor()

    class hb(Thread):
        def __init__(self):
            Thread.__init__(self)
            self.exit = False

        def run(self):
            while not self.exit:
                try:
                    time.sleep(1.5)
                    res = sv.vote_full()
                    s = spd.get_speed()
                    log('[%s] %s %s' % ('CAUTION' if res[1] else 'HEARTBEAT', res[0], s))
                    direction(m, res[0])
                    if sum(s) == 0 and m.status != motor.STATUS_STOP:
                        log('[OBSTACLE] !!!!!')
                        m.do_reverse()
                except KeyboardInterrupt:
                    return
    m.set_speed(int(raw_input('Speed > ') or '10'))
    b = hb()
    b.setDaemon(True)
    b.start()
    #m.go(start = True)

    while True:
        try:
            inp = raw_input('Override >')
            h.do_override(inp)
            if inp == 'b':
                m.back(start = True)
            elif inp == 'g':
                m.go(start = True)
            elif inp == 's':
                m.stop()
        except KeyboardInterrupt:
            break
    b.exit = True
    _logger.q = None
    b.join()
    _logger.join()
    cleanup(m)
