""" separate module for gas sensor """

import RPi.GPIO as GPIO
from gas_detection import GasDetection
import time
import sys

import threading
import logging

class GasSensor(object):

    detection = None # gas instance
    current_result = None

    worker = None
    logger = None
    FILE_PATH = './resources/data/gas.txt'
    stop_thread = False

    def __init__(self, interrupt = True, log_data = True, path = './resources/data/gas.txt' ):
        
        print("Initializing Gas sensor on pin #2(SDA1) and #3(SCL1).")
        print('Calibrating...')
        try:
            GPIO.setmode(GPIO.BCM)
            self.detection = GasDetection()# gas setup

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
                self.worker = threading.Thread(name = "Gas sensor", target = self.__update)
                self.worker.deamon = True
                self.worker.start()
                print("Interrupt enabled.")

        except Exception as e:
            print ("Failed to initalize gas sensor: {}".format(e))
            self.stop_thread = True
            raise e
    

    def detect_gas(self):
        """ Manual get value """
        ppm = self.detection.percentage()

        print('CO: {} ppm'.format(ppm[self.detection.CO_GAS]))

        print('H2: {} ppm'.format(ppm[self.detection.H2_GAS]))

        print('CH4: {} ppm'.format(ppm[self.detection.CH4_GAS]))

        print('LPG: {} ppm'.format(ppm[self.detection.LPG_GAS]))

        print('PROPANE: {} ppm'.format(ppm[self.detection.PROPANE_GAS]))

        print('ALCOHOL: {} ppm'.format(ppm[self.detection.ALCOHOL_GAS]))

        print('SMOKE: {} ppm\n'.format(ppm[self.detection.SMOKE_GAS]))
        

    def __update(self):
        """ Worker function """

        while (not self.stop_thread):
            
            self.current_result = self.detection.percentage()

            if ( self.logger ):
                #self.logger.info(self.current_result)
                self.logger.info('CO: {} ppm. H2: {} ppm. CH4: {} ppm. LPG: {} ppm. PROPANE: {} ppm. ALCOHOL: {} ppm. SMOKE: {} ppm.'.format(
                    self.current_result[self.detection.CO_GAS],
                    self.current_result[self.detection.H2_GAS],
                    self.current_result[self.detection.CH4_GAS],
                    self.current_result[self.detection.LPG_GAS],
                    self.current_result[self.detection.PROPANE_GAS],
                    self.current_result[self.detection.ALCOHOL_GAS],
                    self.current_result[self.detection.SMOKE_GAS]) )

            time.sleep(5)
        
        print("Gas thread ended.")

    def stop(self):
        self.stop_thread = True

    def get_current_h2_result(self):
        """ Poll stored value """
        if (self.current_result):
            return self.current_result[self.detection.H2_GAS] 
        else:
            return -1

