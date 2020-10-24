# This example moves a servo its full range (180 degrees by default) and then back.
from time import sleep
from signal import pause
from board import SCL, SDA

import time
import datetime
import picamera
import os

import busio

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# This example also relies on the Adafruit motor library available here:
# https://github.com/adafruit/Adafruit_CircuitPython_Motor
from adafruit_motor import servo

from camera_processings import ImageSaver
from camera_processings import areEqualImages

swaped = [2]
minValues =  {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
}
maxValues =  {
    0: 180,
    1: 180,
    2: 140,
    3: 180,
    4: 180,
    5: 180,
    6: 180,
    7: 180,
}

def verticaleMove(targetPosition):
    servo0 = servo.Servo(pca.channels[0])
    servo1 = servo.Servo(pca.channels[1])
    if(servo1.angle > 180):
        servo1.angle = 180

    if(servo1.angle < 0):
        servo1.angle = 0

    delta = 1
    diff = 0;
    if(servo1.angle > targetPosition):
        while(servo1.angle > targetPosition):
            if(servo1.angle > targetPosition + delta):
                servo1.angle -= delta
            else:
                servo1.angle = targetPosition
                # servo0.angle 
            # sleep(0.1)
            # servo0.angle = 180 - servo1.angle - 10
            if(180 - servo1.angle - diff < 0):
                servo0.angle = 0
                break;
            elif(180 - servo1.angle - diff > 180):
                # servo0.angle = 180
                break;
            else:
                print(180 - servo1.angle - diff)
                servo0.angle = 180 - servo1.angle - diff
            # sleep(0.1)
    elif(servo1.angle < targetPosition):
        while(servo1.angle < targetPosition):
            if(servo1.angle < targetPosition - delta):
                servo1.angle += delta
            else:
                servo1.angle = targetPosition
                # servo0.angle = diff
                break
            # sleep(0.1)
            if(180 - servo1.angle - diff < 0):
                servo0.angle = 0
                break;
            elif(180 - servo1.angle - diff > 180):
                break;
            else:
                servo0.angle = 180 - servo1.angle - diff
            # sleep(0.1)

def verticaleMove2(targetPosition):
    servo0 = servo.Servo(pca.channels[0])
    servo1 = servo.Servo(pca.channels[1])
    posS0 = int(servo0.angle)
    posS1 = int(servo1.angle)
    if(posS0 < 0):
        posS0 = 0
    elif(posS0 > 180):
        posS0 = 180
    if(posS1 < 0):
        posS1 = 0
    elif(posS1 > 180):
        posS1 = 180
    step = 1
    delta = 0
    if(posS1 < targetPosition):
        while(posS1 < targetPosition - delta):
            if(posS1 + step < targetPosition - delta):
                posS1 += step
            else:
                posS1 = targetPosition - delta

            posS0 = 180 - posS1 - delta
            if(posS0 < 0 or posS0 > 180):
                raise Exception('Not valid data 1')
            servo0.angle = posS0
            servo1.angle = posS1
            sleep(0.1)

    elif(posS1 > targetPosition):
        while(posS1 > targetPosition):
            if(posS1 - step > targetPosition):
                posS1 -= step
            else:
                posS1 = targetPosition + delta

            posS0 = 180 - posS1 - delta
            if(posS0 < 0 or posS0 > 180):
                raise Exception('Not valid data 2')
            servo0.angle = posS0
            servo1.angle = posS1
            sleep(0.1)

def moveServo(index, targetPosition):
    if(index == 0 or index == 1):
        verticaleMove2(targetPosition)
        return

    # if(index == 2 or index == 4):
    if(targetPosition < minValues[index]):
        targetPosition = minValues[index]
    if(targetPosition > maxValues[index]):
        targetPosition = maxValues[index]
    if(index in swaped):
        targetPosition = 180 - targetPosition

    currentServo = servo.Servo(pca.channels[index])
    print(currentServo.angle)
    print(targetPosition)
    if(currentServo.angle > 180):
        currentServo.angle = 180
    if(currentServo.angle < 0):
        currentServo.angle = 0

    delta = 1
    if(currentServo.angle < targetPosition):
        while(currentServo.angle < targetPosition):
            print(currentServo.angle)
            print(targetPosition)
            if(currentServo.angle + delta > targetPosition):
                currentServo.angle = targetPosition
                break;
            else:
                currentServo.angle += delta
    elif(currentServo.angle > targetPosition):
        while(currentServo.angle > targetPosition):
            if(currentServo.angle - delta < targetPosition):
                currentServo.angle = targetPosition
                break;
            else:
                currentServo.angle -= delta


i2c = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c)
pca.frequency = 100

# To get the full range of the servo you will likely need to adjust the min_pulse and max_pulse to
# match the stall points of the servo.
# This is an example for the Sub-micro servo: https://www.adafruit.com/product/2201
# servo7 = servo.Servo(pca.channels[7], min_pulse=580, max_pulse=2480)
# This is an example for the Micro Servo - High Powered, High Torque Metal Gear:
#   https://www.adafruit.com/product/2307
# servo7 = servo.Servo(pca.channels[7], min_pulse=600, max_pulse=2400)
# This is an example for the Standard servo - TowerPro SG-5010 - 5010:
#   https://www.adafruit.com/product/155
# servo7 = servo.Servo(pca.channels[7], min_pulse=600, max_pulse=2500)
# This is an example for the Analog Feedback Servo: https://www.adafruit.com/product/1404
# servo7 = servo.Servo(pca.channels[7], min_pulse=600, max_pulse=2600)

# The pulse range is 1000 - 2000 by default.
servo0 = servo.Servo(pca.channels[0])
servo1 = servo.Servo(pca.channels[1])
servo2 = servo.Servo(pca.channels[2])
servo3 = servo.Servo(pca.channels[3])
servo4 = servo.Servo(pca.channels[4])
servo5 = servo.Servo(pca.channels[5])
servo6 = servo.Servo(pca.channels[6])
servo7 = servo.Servo(pca.channels[7])

# servo2.angle = 20
# servo3.angle = 90
# servo4.angle = 90
# servo5.angle = 5
# servo6.angle = 90
# # servo7.angle = 90
# moveServo(2,50)
# moveServo(3,90)
# moveServo(4,90)
# moveServo(5,20)
# moveServo(6,90)
# verticaleMove2(120)
# print(servo0.angle)
# print(servo1.angle)

def ifGreatThenMoveTo(index, value, targetPosition):
    if(index in swaped):
        targetPosition = 180 - targetPosition
    if(servo.Servo(pca.channels[index]).angle > value):
        moveServo(index, targetPosition)

def ifLessThenMoveTo(index, value, targetPosition):
    if(index in swaped):
        targetPosition = 180 - targetPosition
    if(servo.Servo(pca.channels[index]).angle < value):
        moveServo(index, targetPosition)

def last():
    moveServo(7,90)
    moveServo(5,0)
    moveServo(6,90)
    # moveServo(4,180)
    # verticaleMove2(120)
    ifLessThenMoveTo(0, 120, 120)
    # moveServo(2,90)
    ifGreatThenMoveTo(2, 90, 90)
    verticaleMove2(180)
    moveServo(2,0)
    moveServo(4,90)

# last()    


# def moveStartPosition():
#     #TODO
# def moveCapturePosition1():
#     #TODO
# def moveCapturePosition2():
#     #TODO

# def getTrashIndex():
#     #Send images to PC

#     #Get answer
#     return 0

# def moveToTrash(index):
#     #TODO

# def leaveTrash():
#     #TODO


image = ImageSaver()

controlImagePath = "./images/control.jpeg"
p0ImagePath = "./images/p0.jpeg"
p1ImagePath = "./images/p1.jpeg"
p2ImagePath = "./images/p2.jpeg"

image.Captrue(controlImagePath)
#Control image
while(True):
    image.Captrue(p0ImagePath)

    if(areEqualImages(controlImagePath, p0ImagePath) != True):
        time.sleep(0.5)
        continue

    # moveCampturePosition1()
    # image.Captrue(p1ImagePath)
    # moveCapturePosition1()
    # image.Captrue(p2ImagePath)
    # moveCapturePosition2()

    # trashIndex = getTrashIndex();
    # moveToTrash(trashIndex)
    # leaveTrash()

    # moveStartPosition()



# target = 110
# servo1.angle = 90
# servo0.angle = 90
# servo0.angle = 180 - servo1.angle - 0
# sleep(1)



# delta = 1 if servo1.angle < target else -1
# print(target)
# print(servo1.angle)
# print(int(servo0.angle))
# print(int(servo1.angle))
#for i in range(int(servo1.angle), target):
#    servo0.angle = 180 - i - 0
#    servo1.angle = i
#    sleep(0.05)
#    print(i)


# if(servo1.angle > 180):
#     servo1.angle = 180

# if(servo1.angle < 0):
#     servo1.angle = 0

# delta = 2
# if(servo1.angle > target):
#     while(servo1.angle > target):
#         if(servo1.angle > delta):
#             servo1.angle -= delta
#         else:
#             servo1.angle = 0
#         servo0.angle = 180 - servo1.angle - 0
# elif(servo1.angle < target):
#     while(servo1.angle < target):
#         if(servo1.angle < 180 - delta):
#             servo1.angle += delta
#         else:
#             servo1.angle =180
#         servo0.angle = 180 - servo1.angle - 10