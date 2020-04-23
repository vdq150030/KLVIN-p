#import RPi.GPIO as GPIO
from temperature import *
from pir import * 
#import time


dht = Temperature(4, interrupt = True, log_data = True)
motion = PIR(14)

try:
    while (True):
        print("poll data: {}".format(dht.get_current_temperature()) )
        print("PIR signal : {}.".format(motion.detect_motion()))
        time.sleep(5)
except KeyboardInterrupt:
    GPIO.cleanup()
