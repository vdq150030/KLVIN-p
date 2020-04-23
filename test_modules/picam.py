""" separate module for picamera """

import picamera


class PiCam(object):

    camera = None

    def __init__(self):
        print("Initializing Pi Camera.")
        try:
            self.camera = picamera.PiCamera()
            self.camera.resolution = (640, 480)
        except Exception:
            print ("Failed to initalize Pi Camera: {}".format(Exception))
    

    def record(self, duration = 10, des = '/home/pi/Videos/video.h264'):
        self.camera.start_recording(des)
        self.camera.wait_recording(duration)
        self.camera.stop_recording()
    


