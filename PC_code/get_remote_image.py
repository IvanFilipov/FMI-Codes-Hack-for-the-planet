import urllib.request
from time import sleep
import os

URL =  'http://192.168.2.105/'
LEFT_IMAGE = 'img.jpeg5'
CENTER_IMAGE = 'center.jpg'
RIGHT_IMAGE = 'right.jpg'

def get_remote_image(ulr):
    url_cat = URL + LEFT_IMAGE
    print(url_cat)
    try:
        with urllib.request.urlopen(URL + LEFT_IMAGE) as url:
            img = url.read()
            print(img)
            return img
    except Exception:
        return None

while 1:
    res = get_remote_image(URL)
    if res == None:
        print("none")
        sleep(1)
    else:
        print(res)
    