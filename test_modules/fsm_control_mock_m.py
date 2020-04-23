""" fsm version for testing reduced to 2 states """
import time
import sys

import RPi.GPIO as GPIO
from temperature import *
#from pir import * 
from UltraSonic import *
from picam import *
from humanDetector import *
from flame import *
from sms import *
from Buzzer import *
from gas import *

class FSM (object):
    
    # control loop attr
    state = ""
    running = True

    # devices
    temp_sensor = None
    motion_sensor = None
    camera = None
    human_detector = None
    flame_sensor = None
    sms_service = None
    buzzer = None
    gas_sensor = None

    def __init__(self):
        
        if (self.setup()):
            self.running = True
        else:
            self.temp_sensor.stop()
            self.flame_sensor.stop()
            GPIO.cleanup()
            sys.exit()


    def setup (self):
        """Setup pins, calibrate sensors, initialize variables """
        try:
            self.temp_sensor = Temperature(20, interrupt = True, log_data = True)
            self.motion_sensor = Ultrasonic()
            self.camera = PiCam()
            self.human_detector = Detector()
            self.flame_sensor = FlameSensor(21)
            self.sms_service = SMS()
            self.buzzer = Buzzer(23)
            #self.gas_sensor = GasSensor()
            #if any of this failed -> stop

            print("Setup complete.")
            return True
        except Exception as e:
            print ("Setup Failed. {}".format(e) )
            return False

    #Functions are created for each state with default case
    
    def temp (self):

        print("Entering temperature monitoring state...")

        temp = 0
        while (temp < 30):
            temp = self.temp_sensor.get_current_temperature()
            print ("Current temperature is: {}C".format(temp) )
            time.sleep(1)

        print ("High temperature of {} C".format(temp) )

        self.setState("2") # high temperature. Changes state 

    # time dependence
    def motion (self):

        print("Entering motion sensor state...")

        # When the device enter this state it will dedicate a certain amount of time 
        # to determine whether the stove is occupied or not before it decided to move on to the next state.

        time_left = 30 # time until trigger

        self.setState("") # presumes state changes

        while (time_left > 0):

            motion_signal = self.motion_sensor.get_current_result()

            if (motion_signal):
                print ("Motion detected.")
                self.camera.record()
                if ( self.human_detector.detect()):
                    print ("Stove occupied.")
                    print ("Wait 10 mins..")
                    self.setState("1")
                else:
                    print ("Stove unattended.\n{} more second(s) without human present will trigger the next state.".format(time_left))

            else:
                print ("No motion is detected.\n{} more second(s) without human present will trigger the next state.".format(time_left))
               
            time_left -=1
            time.sleep(1)
    
    def flame (self):
 
        print("Entering flame detection state...")
    
        flame_output = self.flame_sensor.get_current_result()

        if (flame_output):
            print ("Flame detected.")
            self.setState("5")
        else:
            print ("No flame detected.")
            self.setState("4")

        time.sleep(2)

    # time dependence
    def app (self):
 
        print("Entering app alert routine...")
 
        #self.sms_service.send_sms_image(text = "I think your stove is on and unattended. ")
        time.sleep(5)
        self.setState("5")


    def emergency(self):
 
        print("Entering emmergency alert routine...")

        #self.sms_service.send_sms_image(text = "I think your stove is literally on fire. ")
        time.sleep(5)
        self.setState("")

    def Exit(self):

        print("Exit loop")
        # kill all remain threads
        self.temp_sensor.stop()
        self.flame_sensor.stop()
        self.buzzer.stop()
        #self.gas_sensor.stop()
        self.running = False
        
        time.sleep(3) 
        #TODO: get all the thread stop before gpio clean up to prevent error when shutdown
        GPIO.cleanup()
    
    def Default_state (self):
    
        print("Wrong entry! The number must be 1-3")
        self.setState("1")
    
    def run(self):

        # Main control loop
        try:
            while (self.running): 
                self.States.get(self.state,self.Default_state)(self)
                
                # buzzer is active on state 4 and 5 
                if(self.state == "4" or self.state == "5"):
                    self.buzzer.buzz(True)
                else:
                    self.buzzer.buzz(False) 

        except Exception as e:
            GPIO.cleanup()
            raise e 

    def setState(self, s: str):
        self.state = s 

    #Dictionary containing all possible states
    
    States = {
    
        "1": temp, # temp_or_gas
    
        "2": motion,
        
        "3": flame,
        
        "4": app,

        "5": emergency,
    
        "": Exit 
    
        }


# test run
core = FSM()
core.setState("1")

time.sleep(2)
try: 
    core.run()
except:
    core.Exit()
    sys.exit()
