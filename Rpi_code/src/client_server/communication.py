import sys
import threading

sys.path.append('../../../common')

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse, request
from urllib.parse import parse_qs, urlparse

from constants import *

global client_sem
global last_category
client_sem = threading.Semaphore(0)
last_category = 0


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Ok!')
        category = parse_qs(urlparse(self.path).query).get(RPI_HTTP_PARAM, None)
        if category is not None:
            global last_category
            last_category = category[0]
            print(last_category)
            client_sem.release()

def start_HTTP_server():
    httpd = HTTPServer(("", RPI_HTTP_SERVER_PORT), SimpleHTTPRequestHandler)
    httpd.serve_forever()

def get_last_category():
    return last_category

def send_ready_to_PC():
    data = parse.urlencode({"ready": "true"})
    data = data.encode('ascii')
    response = request.urlopen(PC_HTTP_POST_URL, data)
    print("PC response:", response.status)




