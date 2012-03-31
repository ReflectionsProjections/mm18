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

