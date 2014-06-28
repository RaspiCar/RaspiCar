# coding:utf-8
# RPiCar configrations
from RPi import GPIO as io
import os

GPIO_MODE = io.BCM

# pin configurations
PIN_MOTOR_L1 = 27
PIN_MOTOR_L2 = 22

PIN_MOTOR_R1 = 4
PIN_MOTOR_R2 = 17

PIN_PWM = 18 # auto configured

PIN_LEFT_TRACER = 10
PIN_MID_TRACER = 24
PIN_RIGHT_TRACER = 23

PIN_LEFT_LGT = 8 # LGT = light
PIN_RIGHT_LGT = 11

PIN_SPEED_L = 14
PIN_SPEED_R = 15

#wheel circumference in centermeter
WHEEL_C = 22

#web server configurations
PORT = 8080

def getTerminalSize():
    # http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
    try:
        x, y = os.popen('stty size', 'r').read().split()
    except ValueError:
        x, y = 120, 80
    return int(y), int(x)
 
TERM_SIZE = getTerminalSize()