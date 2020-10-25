from enum import Enum

# RPI constants
RPI_HTTP_SERVER_PORT = 8000
RPI_HTTP_PARAM = "category"

RPI_IMG_PATH_CENTER = ""
RPI_IMG_PATH_LEFT   = ""
RPI_IMG_PATH_RIGHT  = ""


# PC constants
PC_IP = "192.168.2.102"
PC_HTTP_POST_URL = "http://%s:1234" % PC_IP

class BinCategory(Enum):
    YELLOW_BIN = 0
    GREEN_BIN  = 1
    BLUE_BIN   = 2
    GRAY_BIN   = 3
    
