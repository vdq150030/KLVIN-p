""" Separate module for Temperature sensor """
import RPi.GPIO as GPIO
import dht11    #temp
import datetime
import time

import threading
import logging


class Temperature(object):
    Temperature_pin = -1
    instance = None
    current_result = None

    worker = None 
    logger = None
    FILE_PATH = './resources/data/temperature.txt' # path is from from where the entry point is. Otherwise get absolute path.
    stop_thread = False

    sampling_rate = 0 # sampling rate = {this value}*3 + 3. 1 min is 19*3 +3

    def __init__(self, tpin, interrupt = False, log_data = False, path = './resources/data/temperature.txt'):

        print("Initializing temperature sensor on pin #{}.".format(tpin))
        try:
            GPIO.setwarnings(True)
            GPIO.setmode(GPIO.BCM)
            self.instance = dht11.DHT11(pin = tpin) # temp setup
            self.Temperature_pin = tpin

            if (log_data):
                self.logger = logging.getLogger(__name__)
                self.logger.setLevel(logging.INFO)
                self.FILE_PATH = path

                formatter = logging.Formatter('%(asctime)s;%(name)s;%(message)s')

                file_handler = logging.FileHandler(path)
                file_handler.setFormatter(formatter)

                self.logger.addHandler(file_handler)
                print ("Logger {} on INFO.".format(__name__))

            if (interrupt):
                self.worker = threading.Thread(name = "Temperature sensor", target = self.__update)
                self.worker.deamon = True
                self.worker.start()
                print("Interrupt enabled.")
            

        except Exception as e:
            print ("Failed to initalize Temperature sensor: {}".format(e))
            # TODO: stop all related thread
            self.stop_thread = True
            raise e
       

    def get_temperature(self):
        """ Manual get value """
        # NOTE: this module have to wait for valid input

        result = None
        while (True):
            result = self.instance.read() 
            if result.is_valid():
            
                print("Last valid input: " + str(datetime.datetime.now()))
                print("Temperature: %d C" % result.temperature)
                print("Temperature: %d F" % ((result.temperature * (9/5)) + 32))
                print("Humidity: %d %%" % result.humidity)
                self.current_result = result.temperature
                if (self.logger):
                    self.logger.info(result.temperature)
                return result.temperature

            time.sleep(3) # dht22 took 2 secs for data

    def __update(self):
        """ Worker function """
        sample = 0

        while (not self.stop_thread):
            
            result = self.instance.read()

            if result.is_valid():
                self.current_result = result
                print("Temperature updated.")

                # NOTE : messy sampling rate logic
                if (self.logger and( sample == self.sampling_rate ) ):
                    self.logger.info(result.temperature)
                    sample = -1

                sample += 1 

            time.sleep(3)

        print("Temperature thread ended.")

    def stop(self):
        self.stop_thread = True

    def get_current_temperature(self):
        """ Poll stored temperature value """
        if (self.current_result):
            return self.current_result.temperature
        else:
            return -1

    def get_current_humidity(self):
        """ Poll stored humidity value """
        if (self.current_result):
            return self.current_result.humidity
        else:
            return -1

