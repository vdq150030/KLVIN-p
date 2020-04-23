""" separate module for kill switch """

import RPi.GPIO as GPIO
import os, sys
import time

# this maybe in the main.py to stop + clean up everything
class Switch(object):

    button_pin = -1

    def __init__(self, pin):
        # set up a pin on gpio interrupt mode.  
        print("Kill switch on pin #{}.".format(pin))
        try:
            GPIO.setmode(GPIO.BCM) # could run into error if setup multiple time ?
            GPIO.setup(pin, GPIO.IN)
            self.button_pin = pin

            # set up interupt on pin       
            GPIO.add_event_detect(self.button_pin,GPIO.BOTH,bouncetime=300)   # let us know when the pin goes HIGH or LOW                          
            # setup interrupt handler
            GPIO.add_event_callback(self.button_pin, self.__callback)  # assign function to GPIO PIN, Run function on change
            
        except Exception as e:
            print ("Failed to setup kill switch: {}".format(e))
            raise e
    
    
    def __callback(self):
        # button pressed. Do stuff
        print ("Button pressed. Throw exception.")
        # TODO: detect hold button
        raise KeyboardInterrupt
        

#!/usr/bin/env python3

# import all important libraries
#from gpiozero import Button
#from signal import pause

# Define GPIO 

red = 19
green = 26
yellow = 16

# Define Commands

def reboot():
    # turn of green flash yellow
	GPIO.cleanup()
	os.system("sudo reboot")
def shutdown():
	# turn of green flash red
	GPIO.cleanup()
	os.system("sudo poweroff")

holdTime = int(3)
# the script
def run_script(self):
    
    pwroff  = Button(21, hold_time=holdTime)
    rst = Button(20, hold_time=holdTime)
    pwroff.when_held = shutdown
    rst.when_held = reboot
    pause()
