#!/usr/bin/env python
# coding:utf-8
# RPiCar controller
from __future__ import print_function
from RPi import GPIO as io
import time
from datetime import datetime
from config import *
from motor import motor
from Sensor import SensorVote, Tracer, Light, HumanOverride

def setup():
    io.setmode(GPIO_MODE)

    io.setup(PIN_LEFT_TRACER, io.IN)
    io.setup(PIN_MID_TRACER, io.IN)
    io.setup(PIN_RIGHT_TRACER, io.IN)

    io.setup(PIN_LEFT_LGT, io.IN)
    io.setup(PIN_RIGHT_LGT, io.IN)

def cleanup(*args):
    io.cleanup()
    for c in args:
        c.cleanup()

def direction(motor, vote):
    if vote == 0:
        motor.go()
    elif vote < 0 :
        motor.turn_left(fast = int(vote) == vote)# fat = without neutral vote
    else:
        motor.turn_right(fast = int(vote) == vote)
    

if __name__ == '__main__':
    from threading import Thread
    setup()
    m = motor()
    sv = SensorVote(new_vote_callback = lambda x:print(datetime.now().strftime('%X') and direction(m, x), '[NEW-VOTE]', x))
    t = Tracer.Tracer()
    sv.add_voter(t)
    l = Light.Light()
    sv.add_voter(l)
    h = HumanOverride.HumanOverride()
    sv.add_voter(h)

    class hb(Thread):
        def __init__(self):
            Thread.__init__(self)
            self.exit = False

        def run(self):
            while not self.exit:
                try:
                    time.sleep(2)
                    res = sv.vote_full()
                    print(datetime.now().strftime('%X'), '[%s]' % ('CAUTION' if res[1] else 'HEARTBEAT'), res[0])
                    direction(m, res[0])
                except KeyboardInterrupt:
                    return
    b = hb()
    b.setDaemon(True)
    b.start()

    m.set_speed(12)
    m.go()

    while True:
        try:
            inp = raw_input('Override >')
            h.do_override(inp)
            if inp == 'b':
                m.back()
            elif inp == 'g':
                m.go()
        except KeyboardInterrupt:
            break
    b.exit = True
    b.join()
    cleanup(m)
