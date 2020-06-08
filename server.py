#!/usr/bin/env python3

from http.server import HTTPServer, CGIHTTPRequestHandler

server_address=("",8800)
httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
httpd.serve_forever()