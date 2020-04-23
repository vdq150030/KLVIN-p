""" Module for buzzer """
import RPi.GPIO as GPIO
import threading
import time

class Buzzer(object):

    buzzer_pin = 23
    frequency = 3000

    worker = None 
    on = False
    stop_thread = False

    def __init__(self, pin, freq=3000):
        print("Buzzer on pin #{}.".format(pin))
        try:
            GPIO.setmode(GPIO.BCM) # could run into error if setup multiple time ?
            GPIO.setwarnings(True)
            GPIO.setup(pin, GPIO.OUT)
            self.buzzer_pin = pin 
            self.frequency = freq

            self.worker = threading.Thread(name = "Smol buzzer", target = self.thread_buzz) # pass arg if necessary
            self.worker.deamon = True
            
        except Exception as e:
            print ("Failed to setup buzzer: {}".format(e))
            self.stop_thread = True
            raise e

    def set_frequency(self, freq):
        self.frequency = freq

    def stop(self):
        self.on = False

    def buzz(self, switch : bool ):
        # be able to call a buzz or stop it. Non blocking.

        if ( switch and not(self.on) ):
            print("buzzer on")
            try:
                self.worker.start()  # can't start the 2nd time 
            except:
                self.worker.run()
            self.on = True

        if ( not(switch) and self.on ):
            print("buzzer off")
            #self.worker._stop() # try to stop
            self.on = False
   
    def thread_buzz(self): # should be running forever
        
        # NOTE: self.frequency doesn't seem to work 
        period = 1.0 / self.frequency                    #in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
        cycle = period*0.5                               #calcuate the time for half of the wave
        print(cycle)
        while (self.on):                                 #start a loop from 0 to the variable "cycles" calculated above
            for i in range(0,self.frequency):
                GPIO.output(self.buzzer_pin, True)       #set pin 27 to high
                time.sleep(cycle)                        #wait with pin 27 high
                GPIO.output(self.buzzer_pin, False)      #set pin 27 to low
                time.sleep(cycle)                        #wait with pin 27 low
            time.sleep(1)

    def manual_buzz(self, frequency=3000, length = 1): # should be running forever
        #buzz(6300,0.15)  # try me

        if(frequency==0):
            time.sleep(length)
            return

        period = 1.0 / frequency                        #in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
        cycle = period*0.5                              #calcuate the time for half of the wave
        numCycles = int(length * frequency)             #the number of waves to produce is the duration times the frequency

        for i in range(numCycles):                      #start a loop from 0 to the variable "cycles" calculated above
            GPIO.output(self.buzzer_pin, True)          #set pin 27 to high
            time.sleep(cycle)                           #wait with pin 27 high
            GPIO.output(self.buzzer_pin, False)         #set pin 27 to low
            time.sleep(cycle)                           #wait with pin 27 low