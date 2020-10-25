import time
import datetime
import os
import math, operator

from functools import reduce
from PIL import ImageChops
from PIL import Image

import picamera
import picamera.array

import cv2
import imutils

BGR_RED = (0, 0, 255)

SEC_BETWEEN_CAPTURES = 2
DIFF_LIMIT = 200

class Camera:
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (960, 540)
        self.last_capture = picamera.array.PiRGBArray(self.camera)
        self.last_full_frame = picamera.array.PiRGBArray(self.camera)
        
    
    def _are_same(self, rhs_capture, lhs_capture, save=False):
        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(rhs_capture, lhs_capture)
        if save:
            tr = 45
            limit = DIFF_LIMIT * 3
        else:
            tr = 30
            limit = DIFF_LIMIT
        thresh = cv2.threshold(frameDelta, tr, 255, cv2.THRESH_BINARY)[1]
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        if save:
            cv2.imwrite("demo_img/base.jpg", rhs_capture)
            cv2.imwrite("demo_img/thresh.jpg", thresh)
            cv2.imwrite("demo_img/frame_delta.jpg", frameDelta)
        
        #time.sleep(SEC_BETWEEN_CAPTURES + 3)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # loop over the contours
        i = 0
        for c in cnts:
            # if the contour is big enough
            if cv2.contourArea(c) >= limit:
                if save:
                    cv2.drawContours(self.last_full_frame, [c], -1, BGR_RED, 5)
                    cv2.imwrite("demo_img/contour.jpg", self.last_full_frame)
                return False
            
        return True
    
    def _get_capture_processed(self):
        with picamera.array.PiRGBArray(self.camera) as cur_capture:
            self.camera.capture(cur_capture, 'rgb')
            frame = cur_capture.array
            self.last_full_frame = frame
            frame = imutils.resize(frame, width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            return gray
    
    def detect_object_blocking(self):
        # get referance image
        self.last_capture = self._get_capture_processed()
        # detect placed
        while True:
            time.sleep(SEC_BETWEEN_CAPTURES)
            print("stepping in")
            next_frame = self._get_capture_processed()
            if not self._are_same(self.last_capture, next_frame):
                self.last_capture = next_frame
                break
        # detect placed and stable
        while True:
            time.sleep(SEC_BETWEEN_CAPTURES)
            print("stablizing...")
            next_frame = self._get_capture_processed()
            if self._are_same(self.last_capture, next_frame, True):
                break
            self.last_capture = next_frame
                
                
    def store_capture(self, image_name: str):
        self.camera.capture(image_name)       
