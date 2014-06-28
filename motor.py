import RPi.GPIO as io
import time
from config import *

class motor(object):
    def __init__(self):
        io.setup(PIN_MOTOR_L1, io.OUT)
        io.setup(PIN_MOTOR_L2, io.OUT)
        io.setup(PIN_MOTOR_R1, io.OUT)
        io.setup(PIN_MOTOR_R2, io.OUT)
        self.setpwm("delayed", "0")
        self.setpwm("mode", "pwm")
        self.setpwm("frequency", "500")
        self.setpwm("active", "1")

    def setpwm(self, property, value):
        try:
            f = open("/sys/class/rpi-pwm/pwm0/" + property, 'w')
            f.write(value)
            f.close()
        except:
            print("Error writing to: " + property + " value: " + value)

    def cleanup(self):
        self.stop()
        self.setpwm("active", "0")

    def go(self):
        io.output(PIN_MOTOR_L1, io.HIGH)
        io.output(PIN_MOTOR_L2, io.LOW)
        io.output(PIN_MOTOR_R1, io.HIGH)
        io.output(PIN_MOTOR_R2, io.LOW)

    def back(self):
        io.output(PIN_MOTOR_L1, io.LOW)
        io.output(PIN_MOTOR_L2, io.HIGH)
        io.output(PIN_MOTOR_R1, io.LOW)
        io.output(PIN_MOTOR_R2, io.HIGH)

    def stop(self):
        io.output(PIN_MOTOR_L1, io.LOW)
        io.output(PIN_MOTOR_L2, io.LOW)
        io.output(PIN_MOTOR_R1, io.LOW)
        io.output(PIN_MOTOR_R2, io.LOW)

    def turn_left(self, fast=True):
        io.output(PIN_MOTOR_L1, io.LOW)
        io.output(PIN_MOTOR_L2, io.HIGH)
        if fast:
            io.output(PIN_MOTOR_R1, io.HIGH)
        else:
            io.output(PIN_MOTOR_R1, io.LOW)
        io.output(PIN_MOTOR_R2, io.LOW)

    def turn_right(self, fast=True):
        io.output(PIN_MOTOR_L1, io.HIGH)
        io.output(PIN_MOTOR_L2, io.LOW)
        io.output(PIN_MOTOR_R1, io.LOW)
        if fast:
            io.output(PIN_MOTOR_R2, io.HIGH)
        else:
            io.output(PIN_MOTOR_R2, io.LOW)

    def set_speed(self, speed):
        '''
        1~20, recommand > 6
        '''
        self.setpwm("duty", str(speed * 5))

if __name__ == '__main__':
    _bind = {'g': go, 'b': back, 'r': turn_right, 'l': turn_left}
    while True:
        try:
            cmd = raw_input("Command, g/r/t/r 0..9, E.g. f5 :")
            d = cmd[0]
            _bind[d]()
            speed = int(cmd[1]) * 11
            #setup("duty", str(speed))
        except KeyboardInterrupt:
            pass

    io.cleanup()