# Using the Ultra Sonic sensor as a motion dector, please report any bugs yo
import RPi.GPIO as GPIO
import time

import threading
import logging

class Ultrasonic(object):

    TRIG = 4
    ECHO = 18
    test = False
    maxDistance = 200
    previousDistance = 0

    current_result = None

    worker = None
    logger = None
    FILE_PATH = './log/data.txt'
    
    def __init__(self, trig = 4, echo = 18, log_data = True, path = './log/ultra.txt'):

        print("Initializing ultrasonic sensor. TRIG on pin #{}, ECHO on pin#{}.".format(trig, echo))

        try:
            self.TRIG = trig
            self.ECHO = echo

            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.TRIG, GPIO.OUT)
            GPIO.setup(self.ECHO, GPIO.IN)

            if (log_data):
                self.logger = logging.getLogger(__name__)
                self.logger.setLevel(logging.INFO)
                self.FILE_PATH = path 

                formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

                file_handler = logging.FileHandler(self.FILE_PATH)
                file_handler.setFormatter(formatter)

                self.logger.addHandler(file_handler)
                print ("Logger {} on INFO.".format(__name__))

        except Exception:
            print ("Failed: {}".format(Exception))


    def get_current_result(self):
        """ return true if motion is detected """ 
        GPIO.output(self.TRIG, True)
        time.sleep(0.0001)
        GPIO.output(self.TRIG, False)

        # Sends out the initial echo signal and starts recording the time
        while GPIO.input(self.ECHO) == False:
            start = time.time()

        # Stops sending the echo signal and records the final time
        while GPIO.input(self.ECHO) == True:
            end = time.time()

        # Calculate the total time it took and the distance it traveled
        deltaTime = end - start
        newDistance = deltaTime/ 0.000058

        # Check for angled errors (Angled errors occur when the echo signal bounces diagonally before it is read again
        # so there is a possibility of randomly getting a distance of 1000 cm while standing still)
        # global test

        test = self.detectMotionV2(self.previousDistance, newDistance)

        self.previousDistance = newDistance


        #time.sleep(1) # will be needed if run as worker thread
        return test
         
    # This version uses a percent error instead of just guessing the ranges like before
    def detectMotionV2(self, previousDistance, newDistance):

        # Using a percent error of 10% cause this sensor is sucky
        errorMargin = ((previousDistance * 0.10) + (previousDistance % 10))
        set = False

        if (previousDistance != 0 and newDistance <= self.maxDistance):
            if (newDistance > previousDistance and (newDistance / previousDistance) < 10):
                set = True
            elif (newDistance < previousDistance and (previousDistance / newDistance) < 10):
                set = True
            else:
                set = False

        if (((newDistance <= (previousDistance - errorMargin)) or (newDistance >= (previousDistance + errorMargin))) and set):
            #self.printMotion(1)
            return True
        else:
            #self.printMotion(0)
            return False

    # Print format for testing
    def printMotion(self, option):
        if option == 1:   
            print('There was motion...')
            #print('Previous Distance: {} cm'.format(previousDistance))
            #print('New Distance: {} cm'.format(newDistance))

        else:
            print('There was no motion...')
            #print('Previous Distance: {} cm'.format(previousDistance))
            #print('New Distance: {} cm'.format(newDistance))

            
        
