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
        path = parsed_path.path
        query = parsed_path.query
        query_dict = dict(parse.parse_qsl(query))
        
        if query_dict['key'] != MOCK_API_KEY:
            self.send_response(403)
            self.end_headers()
            return

        
        # Process an HTTP GET request and return a response with an HTTP 200 status.
        self.send_response(200)
        self.send_header('Content-type','application/json')
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

    resource_path = os.path.join(os.path.dirname(__file__), 'Resources', 
        splitpath[2], splitpath[3], splitpath[4], query['res'],
        splitpath[-1] + '.json')

    with open(resource_path, 'rb') as file:
        content = file.read()
    
    return content
    
def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    _, port = s.getsockname()
    s.close()
    return port


def start_mock_server(port):
    mock_server = HTTPServer(('localhost', port), MockDataPointServer)
    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()


if __name__ == '__main__':
    server = HTTPServer(('localhost', 8080), MockDataPointServer)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()