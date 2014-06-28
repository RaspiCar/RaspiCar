import RPi.GPIO as io
import time

io.setmode(io.BCM)
io_SPEED1 = 14
io_SPEED2 = 15
io.setup(io_SPEED1, io.IN)
io.setup(io_SPEED2, io.IN)

spd = [0, 0]
def speed_callback(pin):
    if pin == io_SPEED1:
        spd[0] += 1
    else:
        spd[1] += 1

def get_speed(pin):
    if pin == io_SPEED1:
        ret = spd[0]
        spd[0] = 0
    else:
        ret = spd[1]
        spd[0] = 0
    return ret

io.add_event_detect(io_SPEED1, io.FALLING, callback = speed_callback)
io.add_event_detect(io_SPEED2, io.FALLING, callback = speed_callback)
while True:
    try:
        print get_speed(io_SPEED1), get_speed(io_SPEED2) 
        time.sleep(1)
    except KeyboardInterrupt:
        break
io.remove_event_detect(io_SPEED1)
io.remove_event_detect(io_SPEED2)
io.cleanup()