from RPi import GPIO as io
from collections import deque
from threading import RLock
from config import *

class speed(object):
    def __init__(self):
        io.setup(PIN_SPEED_L, io.IN)
        io.setup(PIN_SPEED_R, io.IN)
        self._last_time_record = [0, 0]
        self.spd = [deque([0, 0, 0, 0, 0]), deque([0, 0, 0, 0, 0])]
        self.lock = RLock()

    def speed_interrupt(pin):
        if pin == PIN_SPEED_L:
            idx = 0
        elif pin == PIN_SPEED_R:
            idx = 1
        else:
            raise AttributeError(" [%s]speed interrupt can only be called by speed pin events." % self.name)
        self.lock.aquire()
        self.spd[idx].popleft()
        t = time.time()
        self.spd[idx].append(t - self._last_time_record[idx])
        self._last_time_record[idx] = t
        self.lock.release()

    def start_monitor(self):
        io.add_event_detect(PIN_SPEED_L, edge = io.FALLING, callback = self.speed_interrupt)
        io.add_event_detect(PIN_SPEED_R, edge = io.FALLING, callback = self.speed_interrupt)

    def get_raw_speed(self):
        '''
        round per second
        '''
        self.lock.aquire()
        ret = map(lambda x:1/ (4 *sum(x)), self.spd)
        self.lock.release()
        return ret

    def get_speed(self):
        '''
        cm per second
        '''
        return map(lambda x:x * WHEEL_C, self.get_raw_speed())


