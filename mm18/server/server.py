#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn

class MMHandler(BaseHTTPRequestHandler):
	"""
	HTTP request handler for Mechmania
	"""

	## Server Startup Functions

	def __init__(self):
		"""
		Initialize the MMHandler with needed default values.
		"""
		pass


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""
	A basic threaded HTTP server.
	"""

	# Inheriting from ThreadingMixIn automatically gives us the default
	# functions we need for a threaded server.
	pass

# XXX: Temporary for testing purposes, break out into separate file

def Main():
	server = ThreadedHTTPServer(('localhost', 6969), MMHandler)
	# This prevents errors where the socket is still bound
	server.allow_reuse_address = True
	# TODO: Make the server have an option to exit gracefully
	print "Server starting on port 6969"
	server.serve_forever()

if __name__ == '__main__':
	Main()
