import sys
import time
import multiprocessing 
import os

from control import *
from server import *

def run_core(event):
    try:
        core = FSM(event)
        core.setState("1") # for debugging
        core.run()
    except (KeyboardInterrupt, Exception) as e:
        raise e

def run_server(event):
    try:
        tcp_server = TCPServer("192.168.1.19",8000, event)
        tcp_server.run()
    except (KeyboardInterrupt, Exception) as e:
        raise e

def reset_signal_handler():
    pass 

if __name__ == '__main__': # w/o this it might throw an error 

    event = multiprocessing.Event()

    core_process = multiprocessing.Process(name = "core", target=run_core, args=(event,))
    server_process = multiprocessing.Process(name = "server", target=run_server, args=(event,))  

    core_process.start()
    server_process.start()
    
    try:
        while(True):
            time.sleep(5)
            #TODO: user button & handler

    except (KeyboardInterrupt, Exception):
        # TODO: if anything when wrong with either processes, there should be a corresponding routine to handle the case
        print("{} : Exit.".format(__name__)) #TODO: system log

        #second_process.join()
        core_process.terminate()
        server_process.terminate() 
        
        sys.exit()
  
    pass

#import psutil
    # display process info
    #parent = psutil.Process()
    #print("parent:{}; pid:{}; nice: {}".format( __name__, parent.pid, parent.nice() ) )
    #for child in parent.children():
    #    print("child:{}; pid:{}; nice: {}".format( child.__name__, child.pid, child.nice() ) )
        #child.nice(-10)
        #print (child.nice())