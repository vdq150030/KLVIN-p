""" separate module for Flame sensor """

import RPi.GPIO as GPIO
import time
import sys

import threading
import logging

class FlameSensor(object):

    Flame_pin = -1
    current_result = None

    worker = None
    logger = None
    FILE_PATH = './resources/data/events.txt'
    stop_thread = False

    def __init__(self, pin, interrupt = True, log_data = True, path = './resources/data/events.txt', ):
        print("Initializing Flame sensor on pin #{}.".format(pin))
        try:
            GPIO.setmode(GPIO.BCM) # could run into error if setup multiple time ?
            GPIO.setup(pin, GPIO.IN)
            self.Flame_pin = pin

            if (log_data):
                self.logger = logging.getLogger(__name__)
                self.logger.setLevel(logging.INFO)
                self.FILE_PATH = path 

                formatter = logging.Formatter('%(asctime)s;%(name)s;%(message)s')

                file_handler = logging.FileHandler(self.FILE_PATH)
                file_handler.setFormatter(formatter)

                self.logger.addHandler(file_handler)
                print ("Logger {} on INFO.".format(__name__))


            if (interrupt):
                self.worker = threading.Thread(name = "Flame sensor", target = self.__update)
                self.worker.deamon = True
                self.worker.start()
                print("Interrupt enabled.")

        except Exception as e:
            print ("Failed to initalize flame sensor: {}".format(e))
            self.stop_thread = True
            raise e
    

    def detect_flame(self):
        """ Manual get value """
        return GPIO.input(self.Flame_pin)

    def __update(self):
        """ Worker function """

        while (not self.stop_thread):
            
            self.current_result = self.detect_flame()

            if ( self.logger ):
                self.logger.info(self.current_result)

            time.sleep(5)
        
        print("Flame thread ended.")

    def stop(self):
        self.stop_thread = True

    def get_current_result(self):
        """ Poll stored value """
        if (self.current_result):
            return self.current_result
        else:
            return -1

