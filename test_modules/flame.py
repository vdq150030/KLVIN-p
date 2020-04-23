""" separate module for Flame sensor """

import RPi.GPIO as GPIO


class FlameSensor(object):

    Flame_pin = -1

    def __init__(self, pin):
        print("Initializing Flame sensor on pin #{}.".format(pin))
        try:
            GPIO.setmode(GPIO.BCM) # could run into error if setup multiple time ?
            GPIO.setup(pin, GPIO.IN)
            self.Flame_pin = pin

        except Exception as e:
            print ("Failed to initalize flame sensor: {}".format(e))
            raise e
    

    def detect_flame(self):
        return GPIO.input(self.Flame_pin)

