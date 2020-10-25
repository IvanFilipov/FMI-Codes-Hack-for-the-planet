from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse, request
from urllib.parse import parse_qs, urlparse

data = parse.urlencode({"a_key": "a_value"})
data = data.encode('ascii')

url = "http://192.168.2.102:1234"

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Ok!')
        category = parse_qs(urlparse(self.path).query).get('category', None)
        print(category)  # Prints None or the string value of imsi

def 

response = request.urlopen(url, data)
httpd = HTTPServer(("", 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()