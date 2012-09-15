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

		Searches through the urlpatterns to find a URL matching the given path.
		If it finds one, it tries to call it.  Then it breaks out, so it will
		only call the first pattern it matches.  This method calls the
		corresponding function in urlpatterns from urls.py, so expect side
		effects from the game controller.  It also handles serializtion of JSON
		and will send a 400 error if given invalid JSON.  Wil send a 404 if no
		matching URL is found and a 405 if a URL is found but with the wrong
		method.

		method -- string containing the HTTP request method
		"""

		invalid_method = False

		for url in urlpatterns:
			match = re.match(url[0], self.path)

			# check if match is found
			if match:

				# if method is same, process
				if method == url[1]:
					invalid_method = False

					try:
						data = self._process_POST_data(method)
					except ValueError:
						# Invalid JSON
						self.send_error(400)
						return

					# url[2] is the function referenced in the url to call
					# It is called with the group dictionary from the regex
					# and the unrolled JSON data as keyworded arguments
					self.respond(*url[2](match.groupdict(), **data))

					break

				else:
					# Bad method, but valid URL, used for sending 405s
					invalid_method = True

		# Error Handling Below
		# URL found, but not for that method, sending 405 error
		if invalid_method:
			self.send_error(405)
			return

		# no url match found, send 404
		self.send_error(404)
		return

	def do_GET(self):
		"""Handle all GET requests.
		
		On GET request, parse URLs and map them to the API calls."""

		self.match_path("GET")

	def do_POST(self):
		"""Handle all POST requests.
		
		On POST request, parse URLs and map them to the API calls."""

		self.match_path("POST")

	def _process_POST_data(self, method):
		"""Processes the POST data from a request. Private method.

		Reads in a request and returns a dictionary based on whether or not the
		request is a POST request and what POST data the request contains if it
		is.
		
		Throws ValueError on invalid JSON.

		Returns POST data in a dictionary, or empty dictionary on GET.
		"""

		if method == 'POST':
			# POST data should be catured
			length = int(self.headers['Content-Length'])
			input = self.rfile.read(length)
			data = json.loads(input)

		else:
			# GET method, so empty dictionary
			data = {}

		return data

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""A basic threaded HTTP server."""

	# Inheriting from ThreadingMixIn automatically gives us the default
	# functions we need for a threaded server.
	pass
