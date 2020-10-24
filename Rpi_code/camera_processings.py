import time
import datetime
import picamera
import os

from PIL import ImageChops
from PIL import Image
import math, operator
from functools import reduce

class ImageSaver():
    
    def __init__(self):
        self.queue = []
        self.camera = picamera.PiCamera()
        self.camera.resolution = (960, 540)
        self.image_rate = 5
        self.fname = "./images/{}.jpeg"
        self.sleep_rate = 10 #seconds


    def start(self):
        working = True
        while working:       
            try:            
                for i in range(self.image_rate):
                    t = int(time.time())
                    fname = self.fname.format(t)
                    self.capture(fname)
                    self.queue.append(fname)
                    time.sleep(0.5)
                    print(t)
            except Exception:
                pass
            
            time.sleep(self.sleep_rate)
            n = 5
            self.remove_firsts(n)
            print("removed {}".format(n))
                               
       
    def capture(self,image_name):
        self.camera.capture(image_name)
            
    
    def remove_firsts(self,n):
        to_be_removed = self.queue[:n]
        #try:
        for fname in to_be_removed:
            print(fname)
            os.remove(fname)
        #except Exception as e:
           # print("error")
            #print(e)
                
        self.queue = self.queue[n:]
        

def rmsdiff(im1, im2):
    "Calculate the root-mean-square difference between two images"

    h = ImageChops.difference(im1, im2).histogram()

    # calculate rms
    return math.sqrt(reduce(operator.add,
        map(lambda h, i: h*(i**2), h, range(256))
    ) / (float(im1.size[0]) * im1.size[1]))
        

def areEqualImages(firstImagePath, secondImagePath):
    im1 = Image.open(firstImagePath)
    im2 = Image.open(secondImagePath)
    diff = rmsdiff(im1,im2)
    limit = 0.64
    return diff < limit;

if __name__ == "__main__":
    image = ImageSaver()
    image.start()
#    image.start()
    #capture()
   