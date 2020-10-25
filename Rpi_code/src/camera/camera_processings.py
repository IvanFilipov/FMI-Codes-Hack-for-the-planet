import time
import datetime
import os
import math, operator

from functools import reduce
from PIL import ImageChops
from PIL import Image

import picamera
import picamera.array

SEC_BETWEEN_CAPTURES = 2
DIFF_LIMIT = 0.64

class Camera:
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (960, 540)
        self.last_caputre = picamera.array.PiRGBArray(self.camera)    
    
    def _are_same(self, rhs_caputre, lhs_capture):
        "Calculate the root-mean-square difference between two images"
        h = ImageChops.difference(im1, im2).histogram()
    # calculate rms
        return (math.sqrt(reduce(operator.add,
            map(lambda h, i: h*(i**2), h, range(256))
        ) / (float(im1.size[0]) * im1.size[1]))) < DIFF_LIMIT
    
    def detect_object_blocking(self):
        # get referance image
        self.camera.capture(self.last_caputre, 'rgb')
        while True:
            with picamera.array.PiRGBArray(self.camera) as cur_capture:
                time.sleep(SEC_BETWEEN_CAPTURES)
                self.camera.capture(cur_capture, 'rgb')
    
    def store_capture(self, image_name: str):
        self.camera.capture(image_name)       
