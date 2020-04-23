""" fsm version for testing """
import time
import sys 

import RPi.GPIO as GPIO

sys.path.append('./modules')
from modules import temperature, UltraSonic, picam, humanDetector, flame, sms, Buzzer, gas 


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

    event = None

    def __init__(self,ev):

        try:
            self.setup()
            self.running = True
            self.event = ev
        except Exception as e:
            print ("Setup Failed. {}".format(e) )
            self.Exit()
            GPIO.cleanup()
            raise e
            

    def setup (self):
        """Setup pins, calibrate sensors, initialize variables """
        try:
            self.temp_sensor = temperature.Temperature(20, interrupt = True, log_data = True)
            self.motion_sensor = UltraSonic.Ultrasonic()
            self.camera = picam.PiCam()
            self.human_detector =  humanDetector.Detector()
            self.flame_sensor =  flame.FlameSensor(21)
            self.sms_service = sms.SMS()
            self.buzzer =  Buzzer.Buzzer(23)
            #self.gas_sensor =  gas.GasSensor()
            #if any of this failed -> stop

            print("Setup complete.")
        except Exception as e:
            raise e

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

            #if (motion_signal):
            if (True):
                print ("Motion detected.")
                self.camera.record()
                if ( self.human_detector.detect()):
                    print ("Stove occupied.")
                    print ("Wait 10 mins..")
                    #time.sleep(600)
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
        time_left = 30
        
        while (time_left > 0):
            print ("App alert. {} second(s) left.".format(time_left))
            self.event.wait(1)
            time_left -=1
            if (self.event.is_set()):
                self.event.clear()
                self.setState("1")
                return -1

        self.setState("5")


    def emergency(self):
 
        print("Entering emmergency alert routine...")

        #self.sms_service.send_sms_image(text = "I think your stove is literally on fire. ")
        time_left = 30
        
        while (time_left > 0):
            print ("Emergency alert. {} second(s) left.".format(time_left))
            self.event.wait(1)
            time_left -=1
            if (self.event.is_set()):
                self.event.clear()
                self.setState("1")
                return -1

        self.setState("")

    def Exit(self):

        print("{} : Exit loop.".format(__name__))
        # kill all remain threads
        self.temp_sensor.stop()
        self.flame_sensor.stop()
        self.buzzer.stop()
        #self.gas_sensor.stop()
        self.running = False
        
        time.sleep(3) 
        #TODO: get all the thread stop before gpio clean up to prevent error when shutdown
        GPIO.cleanup()
        sys.exit()
    
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

        except KeyboardInterrupt or Exception as e:
            self.Exit()
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

if __name__ == "__main__":

    print("test run") 
    core = FSM()
    core.setState("1")

    time.sleep(2)
    try: 
        core.run()
    except:
        core.Exit()
        sys.exit()
