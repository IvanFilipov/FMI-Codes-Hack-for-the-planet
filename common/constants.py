from enum import Enum

# RPI constants
RPI_HTTP_SERVER_PORT = 8000
RPI_HTTP_PARAM = "category"

RPI_IMG_PATH_CENTER = 'http://192.168.2.105/center.jpg'
RPI_IMG_PATH_LEFT   = 'http://192.168.2.105/left.jpg'
RPI_IMG_PATH_RIGHT  = 'http://192.168.2.105/right.jpg'


# PC constants
PC_IP = "192.168.2.102"
PC_HTTP_POST_URL = "http://%s:1234" % PC_IP

PI_RESPONSE_SERVER_URL = 'http://192.168.2.105:8000/'

class BinCategory(Enum):
    YELLOW_BIN = 0
    GREEN_BIN  = 1
    BLUE_BIN   = 2
    GRAY_BIN   = 3
    
