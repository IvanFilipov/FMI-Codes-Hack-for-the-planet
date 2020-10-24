#!/usr/bin/env python3
from time import sleep
import requests

PI_RESPONSE_SERVER_URL = 'http://192.168.2.105:8000/'
LEFT_IMAGE = 'http://192.168.2.105/left.jpeg'
CENTER_IMAGE = 'http://192.168.2.105/center.jpg'
RIGHT_IMAGE = 'http://192.168.2.105right.jpg'

"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        print("Received Request")
        self.end_headers()
        

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        print(self.headers)
        print("get")
        print("Getting images..")
        # tensorflow get LEFT_IMAGE
        # tensorflow get CENTER_IMAGE
        # tensorflow get RIGHT_IMAGE
        print("Classification....")
        clasification_result = 2 # tesnorflow clasify
        sleep(5) # remove...
        x = requests.get(PI_RESPONSE_SERVER_URL + "?category=" + str(clasification_result))
        print(x.text)
        #self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        # logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
        #         str(self.path), str(self.headers), post_data.decode('utf-8'))
        print("post")
        print(post_data.decode('utf-8'))
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()