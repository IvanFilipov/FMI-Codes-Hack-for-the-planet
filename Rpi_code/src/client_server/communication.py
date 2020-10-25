import sys
sys.path.append('../../../common')

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse, request
from urllib.parse import parse_qs, urlparse

import threading

from constants import *

global client_sem
global last_category

client_sem = threading.Semaphore(0)
last_category = 0

url = "http://192.168.2.102:1234"

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Ok!')
        category = parse_qs(urlparse(self.path).query).get('category', None)
        if category is not None:
            last_category = category[0]
            print(last_category)
            client_sem.release()

def start_HTTP_server():
    httpd = HTTPServer(("", 8000), SimpleHTTPRequestHandler)
    print("started")
    print(CONST)
    httpd.serve_forever()
    

def send_ready_to_PC(pc_url):
    data = parse.urlencode({"ready": "true"})
    data = data.encode('ascii')
    response = request.urlopen(pc_url, data)
    print(response)




