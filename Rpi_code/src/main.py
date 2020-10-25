import sys
import threading

sys.path.append('../../common')

from constants import *
from control.robo_control import *
from client_server.communication import \
     start_HTTP_server, send_ready_to_PC,\
     client_sem, last_category

from camera.camera_processings import Camera

def start_http_server_thread():
    thread = threading.Thread(target = start_HTTP_server)
    thread.daemon = True
    thread.start()




if __name__ == "__main__":
    cam = Camera()
    cam.store_capture("test.jpg")
    sys.exit(0)
    
    start_http_server_thread()
    client_sem.acquire(True) # block for client request
    print("got last category:", last_category)