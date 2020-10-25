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
    
    def get_servo(self, i):
        return servo.Servo(self.pca.channels[i])
        
    def verticaleMoveDoubleGear(self, targetPosition):
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
            self.verticaleMoveDoubleGear(targetPosition)
            return

        # if(index == 2 or index == 4):
        if (targetPosition < self.minValues[index]):
            targetPosition = self.minValues[index]
        if (targetPosition > self.maxValues[index]):
            targetPosition = self.maxValues[index]
        if (index in self.swaped):
            targetPosition = 180 - targetPosition

        currentServo = servo.Servo(self.pca.channels[index])
        # print(currentServo.angle)
        # print(targetPosition)
        if (currentServo.angle > 180):
            currentServo.angle = 180
        if (currentServo.angle < 0):
            currentServo.angle = 0

        delta = 1
        if (currentServo.angle < targetPosition):
            while (currentServo.angle < targetPosition):
                # print(currentServo.angle)
                # print(targetPosition)
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

# all angles are in absolute coordinates!
# base rotation
JOINT_BASE = 7
TITA_7_BASE = 90

JOINT_GRIPPER_GRAP = 5
TITA_5_BASE = 0  # gripper

JOINT_ROTATE_GRIPPER = 6
TITA_6_BASE = 90

JOINT_DOUBLE_GEAR = 0
TITA_0_BASE = 120
TITA_0_BASE_1 = 180 

JOINT_ELBOL = 2
TITA_2_BASE = 90
TITA_2_BASE_1 = 0

JOINT_UPPER_ELBOL = 4
TITA_4_BASE = 60

JOINT_SHOULDER = 3
TITA_3_BASE = 90

TOTAL_JOINTS_CNT = 7

class RobotController:
    
    def __init__(self):
        self.pos = 0
        self.servo_controler = ServoController()
    
    def debug_info(self):
        for i in range(TOTAL_JOINTS_CNT + 1):
            currentServo = self.servo_controler.get_servo(i)
            print("JOINT %d - angle %f" % (i, currentServo.angle))
    
    def go_to_home_pos(self):
        # OK
        self.servo_controler.moveServo(JOINT_BASE, TITA_7_BASE)
        self.servo_controler.moveServo(JOINT_GRIPPER_GRAP, TITA_5_BASE)
        self.servo_controler.moveServo(JOINT_ROTATE_GRIPPER, TITA_6_BASE)
        self.servo_controler.ifLessThenMoveTo(JOINT_DOUBLE_GEAR, TITA_0_BASE, TITA_0_BASE)
        self.servo_controler.ifGreatThenMoveTo(JOINT_ELBOL, TITA_2_BASE, TITA_2_BASE)
        self.servo_controler.verticaleMoveDoubleGear(TITA_0_BASE_1)
        self.servo_controler.moveServo(JOINT_ELBOL, TITA_2_BASE_1)
        self.servo_controler.moveServo(JOINT_UPPER_ELBOL, TITA_4_BASE)
        self.servo_controler.moveServo(JOINT_SHOULDER, TITA_3_BASE)
        sleep(1)
        
    def go_to_capture_left_pos(self):
        self.servo_controler.moveServo(JOINT_BASE, TITA_7_BASE + 5)
        sleep(0.5)        
        print("left capture")
        
    def go_to_capture_right_pos(self):
        self.servo_controler.moveServo(JOINT_BASE, TITA_7_BASE - 5)
        sleep(0.5)
        print("right capture")
    
    def go_to_center(self):
        self.servo_controler.moveServo(JOINT_BASE, TITA_7_BASE)
        
    def go_to_bin_pos(self, bin_num):
        if bin_num == 1:
            self.servo_controler.moveServo(JOINT_BASE, TITA_7_BASE + 20)
            self.servo_controler.verticaleMoveDoubleGear(TITA_0_BASE_1 - 20)
            sleep(1)
            self.go_to_center()
            self.servo_controler.verticaleMoveDoubleGear(TITA_0_BASE_1)
            sleep(1)
        if bin_num == 2:
            self.servo_controler.moveServo(JOINT_BASE, TITA_7_BASE + 10)
            self.servo_contorler.moveServo(JOINT_UPPER_ELBOL, TITA_4_BASE - 10)
            sleep(1)
            self.go_to_center()
            self.servo_contorler.moveServo(JOINT_UPPER_ELBOL, TITA_4_BASE)
            sleep(1)
        if bin_num == 3:
            self.servo_controler.moveServo(JOINT_BASE, TITA_7_BASE - 10)
            self.servo_contorler.moveServo(JOINT_UPPER_ELBOL, TITA_4_BASE - 10)
            sleep(1)
            self.go_to_center()
            self.servo_contorler.moveServo(JOINT_UPPER_ELBOL, TITA_4_BASE)
            sleep(1)
        if bin_num == 4:
            self.servo_controler.moveServo(JOINT_BASE, TITA_7_BASE - 20)
            self.servo_controler.verticaleMoveDoubleGear(TITA_0_BASE_1 - 20)
            sleep(1)
            self.go_to_center()
            self.servo_controler.verticaleMoveDoubleGear(TITA_0_BASE_1)
            sleep(1)
        