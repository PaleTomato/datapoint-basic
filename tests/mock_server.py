from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import socket
from threading import Thread
from urllib import parse

import requests

MOCK_API_KEY = 'abcdefg'

class MockDataPointServer(BaseHTTPRequestHandler):
    def do_GET(self):

        parsed_path = parse.urlparse(self.path)
        path = parsed_path.path # e.g. /public/data/val/wxfcs/all/json/capabilities
        query = parsed_path.query # res=3hourly&key=abcde
        query_dict = dict(parse.parse_qsl(query))
        
        if query_dict['key'] != MOCK_API_KEY:
            self.send_response(403)
            self.end_headers
            return

        
        # Process an HTTP GET request and return a response with an HTTP 200 status.
        self.send_response(200)
        self.end_headers()
        self.wfile.write(get_json_from_path(path, query_dict))

        return

def get_json_from_path(path, query):
    """
    Convert a url path to a directory reference and return the json.
    """

    # Split out the path and remove empty elements
    splitpath = path.split('/')
    splitpath = list(filter(None, splitpath))

    resource_path = os.path.join('Resources',splitpath[2], splitpath[3],
        splitpath[4], query['res'], splitpath[-1] + '.json')

    with open(resource_path, 'rb') as file:
        content = file.read()
    
    return content
    

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8080), MockDataPointServer)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()