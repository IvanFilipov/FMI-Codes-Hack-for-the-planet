import sys
import threading

sys.path.append('../../common')

from constants import *

from client_server.communication import \
     start_HTTP_server, send_ready_to_PC,\
     client_sem, last_category

from camera.camera_processings import Camera
from control.robo_control import RobotController

def start_http_server_thread():
    thread = threading.Thread(target = start_HTTP_server)
    thread.daemon = True
    thread.start()

def block_until_object_detection(cam):
    cam.detect_object_blocking()

def capture_object_from_diff_angles(cam, robo):
    cam.store_capture(RPI_IMG_PATH_CENTER)
    robo.go_to_capture_left_pos()
    cam.store_capture(RPI_IMG_PATH_LEFT)
    robo.go_to_capture_right_pos()
    cam.store_capture(RPI_IMG_PATH_RIGHT)
    
    
    


if __name__ == "__main__":
    print("Initialization...")
    cam  = Camera()
    robo = RobotController()
    start_http_server_thread()
    
    while True:
        print("Returning to home position...")
        robo.go_to_home_pos()
        
        print("Detecting object...")
        block_until_object_detection(cam)
    
        print("Making some captures of the object...")
        capture_object_from_diff_angles(cam, robo)
    
        print("Telling the PC that we are ready with image processing...")
        send_ready_to_PC()
    
        print("Blocking until the object is classified by the PC...")
        client_sem.acquire(True) # block for client request
    
        print("Going to bin: ", last_category)
        robo.go_to_bin_pos(last_category)