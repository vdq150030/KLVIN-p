""" separate module for picamera """

import picamera


class PiCam(object):

    camera = None
    FILE_PATH = './resources/video.h264'

    def __init__(self, res = (640,480), path = './resources/video.h264'):
        print("Initializing Pi Camera\n")
        try:
            self.camera = picamera.PiCamera()
            self.camera.resolution = (640, 480)
            self.FILE_PATH = path
        except Exception as e:
            print ("Failed to initalize Pi Camera: {}".format(e))
            raise e

        print("Camera resolution is set to {}.\nRecorded files will be in {}".format(res, self.FILE_PATH))

    def get_filepath(self):
        return self.FILE_PATH

    def set_filepath(self, path):
        self.FILE_PATH = path    

    def record(self, duration = 10, des = './resources/video.h264'):
        print("recording")
        try:
            self.camera.start_recording(self.FILE_PATH)
            self.camera.wait_recording(duration)
            self.camera.stop_recording()
            print("File recorded at {}. Duration {}s".format(self.FILE_PATH, duration) )
        except Exception as e:
            print ("Error while recording.")
            raise e
    


