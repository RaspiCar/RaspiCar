import RPi.GPIO as io
import time

io.setmode(io.BCM)
io_DATA1 = 4
io_DATA2 = 17
io_DATA3 = 27
io_DATA4 = 22

output = io.output

io.setup(io_DATA1, io.OUT)
io.setup(io_DATA2, io.OUT)
io.setup(io_DATA3, io.OUT)
io.setup(io_DATA4, io.OUT)

# io.setup(io_CTRL,io.OUT)

time.sleep(1)


def setup(property, value):
    try:
        f = open("/sys/class/rpi-pwm/pwm0/" + property, 'w')
        f.write(value)
        f.close()
    except:
        print("Error writing to: " + property + " value: " + value)
setup("delayed", "0")
setup("mode", "pwm")
setup("frequency", "500")
setup("active", "1")


def go():
    output(io_DATA1, io.HIGH)
    output(io_DATA2, io.LOW)
    output(io_DATA3, io.HIGH)
    output(io_DATA4, io.LOW)


def back():
    output(io_DATA1, io.LOW)
    output(io_DATA2, io.HIGH)
    output(io_DATA3, io.LOW)
    output(io_DATA4, io.HIGH)


def turn_left(fast=True):
    output(io_DATA1, io.LOW)
    output(io_DATA2, io.HIGH)
    if fast:
        output(io_DATA3, io.HIGH)
    else:
        output(io_DATA3, io.LOW)
    output(io_DATA4, io.LOW)


def turn_right(fast=True):
    output(io_DATA1, io.HIGH)
    output(io_DATA2, io.LOW)
    output(io_DATA3, io.LOW)
    if fast:
        output(io_DATA4, io.HIGH)
    else:
        output(io_DATA4, io.LOW)

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
