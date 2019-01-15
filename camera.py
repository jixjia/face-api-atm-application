#!/usr/bin/env python
import cv2, subprocess, config, time
from random import randint

face_cascade = cv2.CascadeClassifier('trained_frontalface_default.xml')
alpha = 40
scaleFactor = 0.5

class SecurityCam(object):

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
    
    def __del__(self):
        self.cap.release()
    
    def release(self):
        self.cap.release()

    def input(self):
        
        _, img = self.cap.read()

        '''Resize image to speed up processing'''
        resizedImg = cv2.resize(img, None, fx = scaleFactor, fy = scaleFactor)

        grayImg = cv2.cvtColor(resizedImg, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(grayImg, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))
        
        # Process found faces
        for (x, y, w, h) in faces:
            
            config.humanPresence = True

            # Scale coordiantes for image crop
            xi = int(x * round(1/scaleFactor,1))
            yi = int(y * round(1/scaleFactor,1))
            wi = int(w * round(1/scaleFactor,1))
            hi = int(h * round(1/scaleFactor,1))

            if config.frameNum % config.intervalRate == 0 or config.frameNum == 10:
                cv2.imwrite(config.directory+'/'+config.faceSession+'/'+str(config.frameNum)+'.jpg',img[yi-alpha:yi+hi+alpha,xi-alpha:xi+wi+alpha])
                config.capturedImages += 1
                
                '''Asynchrnously process face using Face API (invoke face-api.py)'''
                
                # cmd = 'python test-console.py'
                # p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
                # output, errors = p.communicate()

            config.frameNum += 1

        
        _, mjpeg = cv2.imencode('.jpg', resizedImg)

        return mjpeg.tobytes()
