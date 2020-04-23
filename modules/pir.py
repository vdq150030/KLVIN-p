""" Separate module for PIR """

import RPi.GPIO as GPIO
import time
import sys

import threading
import logging

class PIR(object):
    
    PIR_pin = -1
    current_result = None

    worker = None
    logger = None
    FILE_PATH = './resources/data/pir.txt'

    def __init__(self, pin, interrupt = True, log_data = True, path = './resources/data/pir.txt'):
        """ Setup on pin. Interrupt and logging enabled by default. """

        print("Initializing PIR on pin #{}.".format(pin))
        try:
            GPIO.setmode(GPIO.BCM) # could run into error if setup multiple time ?
            GPIO.setup(pin, GPIO.IN)
            self.PIR_pin = pin


            if (log_data):
                self.logger = logging.getLogger(__name__)
                self.logger.setLevel(logging.INFO)
                self.FILE_PATH = path 

                formatter = logging.Formatter('%(asctime)s;%(levelname)s;%(name)s;%(message)s')

                file_handler = logging.FileHandler(self.FILE_PATH)
                file_handler.setFormatter(formatter)

                self.logger.addHandler(file_handler)
                print ("Logger {} on INFO.".format(__name__))


            if (interrupt):
                self.worker = threading.Thread(name = "PIR sensor", target = self.__update)
                self.worker.deamon = True
                self.worker.start()
                print("Interrupt enabled.")

        except Exception as e:
            print ("Failed to initalize PIR: {}".format(e))
            raise e
    

    def detect_motion(self):
        """ Manual get value """
        return GPIO.input(self.PIR_pin)

    def __update(self):
        """ Worker function """

        while (True):
            
            self.current_result = GPIO.input(self.PIR_pin)

            if ( self.logger ):
                self.logger.info(self.current_result)

            time.sleep(1)


    def get_current_value(self):
        """ Poll stored value """
        if (self.current_result):
            return self.current_result
        else:
            return -1