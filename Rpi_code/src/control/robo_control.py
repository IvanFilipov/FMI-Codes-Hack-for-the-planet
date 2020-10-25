from time import sleep
from signal import pause
from board import SCL, SDA

import time
import datetime
import os

import busio

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# This example also relies on the Adafruit motor library available here:
# https://github.com/adafruit/Adafruit_CircuitPython_Motor
from adafruit_motor import servo

class ServoController:
    
    def __init__(self):
        self.pos = 0
        self.swaped = [2]
        self.minValues =  {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
        }
        self.maxValues =  {
            0: 180,
            1: 180,
            2: 140,
            3: 180,
            4: 180,
            5: 180,
            6: 180,
            7: 180,
        }

        self.i2c = busio.I2C(SCL, SDA)

        # Create a simple PCA9685 class instance.
        self.pca = PCA9685(self.i2c)
        self.pca.frequency = 100

        self.servo0 = servo.Servo(self.pca.channels[0])
        self.servo1 = servo.Servo(self.pca.channels[1])
        self.servo2 = servo.Servo(self.pca.channels[2])
        self.servo3 = servo.Servo(self.pca.channels[3])
        self.servo4 = servo.Servo(self.pca.channels[4])
        self.servo5 = servo.Servo(self.pca.channels[5])
        self.servo6 = servo.Servo(self.pca.channels[6])
        self.servo7 = servo.Servo(self.pca.channels[7])
        
    def verticaleMove(self, targetPosition):
        if (targetPosition > 175):
            targetPosition = 175

        servo0 = servo.Servo(self.pca.channels[0])
        servo1 = servo.Servo(self.pca.channels[1])
        posS0 = int(servo0.angle)
        posS1 = int(servo1.angle)
        if (posS0 < 0):
            posS0 = 0
        elif (posS0 > 180):
            posS0 = 180
        if (posS1 < 0):
            posS1 = 0
        elif (posS1 > 180):
            posS1 = 180
        step = 1
        delta = 0
        if (posS1 < targetPosition):
            while (posS1 < targetPosition - delta):
                if (posS1 + step < targetPosition - delta):
                    posS1 += step
                else:
                    posS1 = targetPosition - delta

                posS0 = 180 - posS1 - delta
                if (posS0 < 0 or posS0 > 180):
                    raise Exception('Not valid data 1')
                servo0.angle = posS0
                servo1.angle = posS1
                sleep(0.1)

        elif (posS1 > targetPosition):
            while (posS1 > targetPosition):
                if (posS1 - step > targetPosition):
                    posS1 -= step
                else:
                    posS1 = targetPosition + delta

                posS0 = 180 - posS1 - delta
                if (posS0 < 0 or posS0 > 180):
                    raise Exception('Not valid data 2')
                servo0.angle = posS0
                servo1.angle = posS1
                sleep(0.1)

    def moveServo(self, index, targetPosition):
        if (index == 0 or index == 1):
            self.verticaleMove(targetPosition)
            return

        # if(index == 2 or index == 4):
        if (targetPosition < self.minValues[index]):
            targetPosition = self.minValues[index]
        if (targetPosition > self.maxValues[index]):
            targetPosition = self.maxValues[index]
        if (index in self.swaped):
            targetPosition = 180 - targetPosition

        currentServo = servo.Servo(self.pca.channels[index])
        print(currentServo.angle)
        print(targetPosition)
        if (currentServo.angle > 180):
            currentServo.angle = 180
        if (currentServo.angle < 0):
            currentServo.angle = 0

        delta = 1
        if (currentServo.angle < targetPosition):
            while (currentServo.angle < targetPosition):
                print(currentServo.angle)
                print(targetPosition)
                if (currentServo.angle + delta > targetPosition):
                    currentServo.angle = targetPosition
                    break;
                else:
                    currentServo.angle += delta
        elif (currentServo.angle > targetPosition):
            while (currentServo.angle > targetPosition):
                if (currentServo.angle - delta < targetPosition):
                    currentServo.angle = targetPosition
                    break;
                else:
                    currentServo.angle -= delta

    def ifGreatThenMoveTo(self, index, value, targetPosition):
        if (index in self.swaped):
            targetPosition = 180 - targetPosition
        if (servo.Servo(self.pca.channels[index]).angle > value):
            self.moveServo(index, targetPosition)

    def ifLessThenMoveTo(self, index, value, targetPosition):
        if (index in self.swaped):
            targetPosition = 180 - targetPosition
        if (servo.Servo(self.pca.channels[index]).angle < value):
            self.moveServo(index, targetPosition)

class RobotController:
    
    def __init__(self):
        self.pos = 0
        self.servo_controler = ServoController()
        
    def go_to_home_pos(self):
        print("home")
        
    def go_to_capture_left_pos(self):
        print("left capture")
        
    def go_to_capture_right_pos(self):
        print("right capture")
        
    def go_to_bin_pos(self, bin_num):
        print("going to ", bin_num)
        