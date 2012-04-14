from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import re, json

from urls import urlpatterns

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

	def respond(self, data):
		"""
		Responds by sending JSON data back.
		"""
		self.send_response(data['status_code'])
		output = json.encode(data)
		self.send_header("Content-type", "application/json")
		self.end_headers()
		self.wfile.write(output)

	def match_path(self, method):
		"""
		Tries to match a path with every url in urlpatterns.
		If it finds one, it tries to call it.  Then it breaks out, 
		so it will only call the first pattern it matches.
		"""
		matched_url = False
		for url in urlpatterns:
			match = re.match(url[0], self.path)
			if match and method == url[1]:
				self.respond(url[2](match.groupdict(), json.loads(self.rfile.read())
				matched_url = True
				break
		if not matched_url:
			self.send_error(404)

	def do_GET(self):
		"""
		Handle all GET requests here by parsing URLs and mapping them
		to the API calls.
		"""
		self.match_path("GET")

	def do_POST(self):
		"""
		Handle all POST requests here by parsing URLs and mapping them
		to the API calls.
		"""
		self.match_path("POST")

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""
	A basic threaded HTTP server.
	"""

	# Inheriting from ThreadingMixIn automatically gives us the default
	# functions we need for a threaded server.
	pass
