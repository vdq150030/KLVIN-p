# open video file and detect human face
# notice class vs static functions
# async : may be but unlikely. More like threading.
import numpy as np
import cv2
import sys

class Detector:

    faceCascade = None 

    def __init__(self, cascPath = 'haarcascade_frontalface_default.xml'):
        
        try:
            print("Loading face cascade from {}".format(cascPath) )
            # Create the haar cascade
            self.faceCascade = cv2.CascadeClassifier(cascPath)
            print ("Initialzing camera..")
            #TODO: have a test camera routine 

        except Exception as e:
            print('Failed to initialize module: {}'.format(e))
            raise e

        pass

    def detect(self,filepath = 'video.mp4'):
        ''' Analyze input video and return true/false if face detected '''
        print ("Reading file")
        cap = cv2.VideoCapture('video.mp4') # arg doesn't works

        while(cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = cap.read()
            if (not ret):
                # end of file 
                break
            
            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if (self.__detect_faces(gray)>0):
                print ("Face detected")
                return True
            
            # Display the resulting frame
            cv2.imshow('frame',gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

        return False

    def __detect_faces(self, frame):
        # Detect faces in the image
        faces = self.faceCascade.detectMultiScale(
        frame,
        scaleFactor=1.1,
        #minNeighbors=5,
        #minSize=(30, 30),
        #flags = cv2.CASCADE_SCALE_IMAGE
        )
        #print (" Found {0} faces!".format(len(faces)))

        return len(faces)