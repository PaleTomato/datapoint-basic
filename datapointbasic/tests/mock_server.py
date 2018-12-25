from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import socket
from threading import Thread
from urllib import parse

MOCK_API_KEY = 'abcdefg'


class MockDataPointServer(BaseHTTPRequestHandler):
    """
    Mock DataPoint server that returns canned data based on request.
    """
    def do_GET(self):

        parsed_path = parse.urlparse(self.path)
        path = parsed_path.path
        query = parsed_path.query
        query_dict = dict(parse.parse_qsl(query))

        if query_dict['key'] != MOCK_API_KEY:
            self.send_response(403)
            self.end_headers()
            return

        # Return a response with an HTTP 200 status.
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(get_json_from_path(path, query_dict))

        return


class MockDataPointRequest(object):
    """
    Class that mocks the DataPointRequest object using canned data.
    """

    def __init__(self, val, wx, item, feed, params={}):
        """
        Initialise the object
        """

        self.val = val
        self.wx = wx
        self.item = item
        self.feed = feed
        self.params = params

    @property
    def json(self):
        """
        Return the json from the request (from the canned data).
        """

        resource_path = os.path.join(os.path.dirname(__file__),
                                     'Resources',
                                     self.val,
                                     self.wx,
                                     self.item,
                                     self.params['res'],
                                     self.feed + '.json')

        with open(resource_path, 'r') as file:
            content = json.load(file)

        return content


def get_json_from_path(path, query):
    """
    Convert a url path to a directory reference and return the json.
    """

    # Split out the path and remove empty elements
    splitpath = path.split('/')
    splitpath = list(filter(None, splitpath))

    resource_path = os.path.join(os.path.dirname(__file__),
                                 'Resources',
                                 splitpath[2],
                                 splitpath[3],
                                 splitpath[4],
                                 query['res'],
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


def start_mock_server():
    port = get_free_port()
    mock_url = 'http://localhost:{port}'.format(port=port)
    mock_server = HTTPServer(('localhost', port), MockDataPointServer)
    mock_server_thread = Thread(target=mock_server.serve_forever,
                                daemon=True)
    mock_server_thread.start()
    return (mock_server, mock_url)


if __name__ == '__main__':
    SERVER = HTTPServer(('localhost', 8080), MockDataPointServer)
    print('Starting server, use <Ctrl-C> to stop')
    SERVER.serve_forever()
