from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import re, json

from urls import urlpatterns

class MMHandler(BaseHTTPRequestHandler):
	"""HTTP request handler for Mechmania"""

	## Server Startup Functions

	def respond(self, status_code, data):
		"""
		Responds by sending JSON data back.

		status_code -- string containting HTTP status code.
		data -- dictionary to encode to JSON
		"""
		self.send_response(int(status_code))
		output = json.dumps(data)
		self.send_header("Content-type", "application/json")
		self.end_headers()
		self.wfile.write(output)

	def match_path(self, method):
		"""Tries to match a path with every url in urlpatterns.
		If it finds one, it tries to call it.  Then it breaks out, 
		so it will only call the first pattern it matches.  This method
		calls the corresponding function in urlpatterns from urls.py, so
		expect side effects from the game controller.  It also handles
		serializtion of JSON and will send a 400 error if given invalid
		JSON.  Wil send a 404 if no matching URL is found and a 405 if 
		a URL is found but with the wrong method.

		method - string containing the HTTP request method
		"""
		matched_url = False
		invalid_method = False
		invalid_JSON = False
		for url in urlpatterns:
			match = re.match(url[0], self.path)
			# check if match is found
			if match:
				# if method is same, process
				if method == url[1]:
					# POST data should be catured
					if method == 'POST':
						try:
							length = int(self.headers['Content-Length'])
							input = self.rfile.read(length)
							data = json.loads(input)
						except ValueError:
							# invalid JSON, send 400 error
							invalid_JSON = True
					# GET method, so empty dictionary
					else:
						data = {}
					# Send a response based on return from function
					# first arg to url[2] is the matches pulled from url
					# second arg is unrolled data dictionary
					if not invalid_JSON:
						self.respond(*url[2](match.groupdict(), **data))
					# We found a URL, used for 404s later
					matched_url = True
					# It has a valid method, used for 405s later
					invalid_method = False
					break
				# Bad method, but valid URL, used for sending 405s
				else:
					matched_url = True
					invalid_method = True
		# Error Handling Below
		# no url match found, send 404
		if not matched_url:
			self.send_error(404)
		# URL found, but not for that method, sending 405 error
		if matched_url and invalid_method:
			self.send_error(405)
		if invalid_JSON:
			self.send_error(400)

	def do_GET(self):
		"""Handle all GET requests here by parsing URLs and mapping them to the API calls."""
		self.match_path("GET")

	def do_POST(self):
		"""Handle all POST requests here by parsing URLs and mapping them to the API calls."""
		self.match_path("POST")

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""A basic threaded HTTP server."""

	# Inheriting from ThreadingMixIn automatically gives us the default
	# functions we need for a threaded server.
	pass
