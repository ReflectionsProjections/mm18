from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn

import re
import json

from urls import urlpatterns
from client_manager import MMClientManager
from mm18.game.game_controller import init_game

global_client_manager = MMClientManager()

class MMHandler(BaseHTTPRequestHandler):
	"""HTTP request handler for Mechmania"""

	def respond(self, status_code, data):
		"""
		Responds by sending JSON data back.

		status_code -- string containting HTTP status code.
		data -- dictionary to encode to JSON
		"""

		self.send_response(int(status_code))
		# API defines status as being a part of the JSON going out
		if 'status' not in data:
			data['status'] = status_code
		output = json.dumps(data)
		self.send_header("Content-type", "application/json")
		self.end_headers()
		self.wfile.write(output)

	def match_path(self):
		"""Tries to match a path with every url in urlpatterns.

		Searches through the urlpatterns to find a URL matching the given path.
		If it finds one, it tries to call it.  Then it breaks out, so it will
		only call the first pattern it matches.  This method calls the
		corresponding function in urlpatterns from urls.py, so expect side
		effects from the game controller.  It also handles serializtion of JSON
		and will send a 400 error if given invalid JSON.  Wil send a 404 if no
		matching URL is found.
		"""

		# Special case connection. Shut up I know it's ugly.
		connect_match = re.match(r'/connect', self.path)
		if connect_match:
			self._connect_client()
			return

		# Get the data from the method
		try:
			data = self._process_POST_data()
		except ValueError:
			# Invalid JSON
			self.send_error(400)
			return

		# Every call but connect requires authorization
		if not self._validate_client(data):
			return

		for url in urlpatterns:
			match = re.match(url[0], self.path)

			# check if match is found
			if match:

				# url[2] is the function referenced in the url to call
				# It is called with the group dictionary from the regex
				# and the unrolled JSON data as keyworded arguments
				# A two-tuple is returned, which is unrolled and passed as
				# arguments to respond
				self.respond(*url[2](match.groupdict(), **data))
				return

		# no url match found, send 404
		self.send_error(404)
		return

	def do_GET(self):
		"""Handle all GET requests.
		
		On GET request, parse URLs and map them to the API calls."""

		self.send_error(405)
		return

	def do_POST(self):
		"""Handle all POST requests.
		
		On POST request, parse URLs and map them to the API calls."""

		self.match_path()

	def _process_POST_data(self):
		"""Processes the POST data from a request. Private method.

		Reads in a request and returns a dictionary based on whether or not the
		request is a POST request and what POST data the request contains if it
		is.
		
		Throws ValueError on invalid JSON.

		Returns POST data in a dictionary.
		"""

		length = int(self.headers['Content-Length'])
		input = self.rfile.read(length)
		data = json.loads(input)

		return data

	def _connect_client(self):
		"""Connect a new client to the game.

		When a client attempts to connect we connect them to the game if
		allowed (not already connected, server is not full).
		"""

		print "Connecting client"
		client = global_client_manager.add_client()
		if client is None:
			# Server is full, no connection for you!
			self.respond(403, {'error': 'Server is full'})
			return

		# Prepare the dictionary to send back to the user
		reply = {}
		reply['id'] = client[0]
		reply['auth'] = client[1]
		self._wait_for_game_init(reply)

	def _wait_for_game_init(self, reply):
		"""Wait for the game to start before returning to the client.

		After a client has joined the game, we wait for the game to start
		before sending them back information about the game.
		"""
		# Get the run lock on the client manager
		global_client_manager.game_condition.acquire()
		if global_client_manager.is_full():
			print "Game is full, starting"
			# Start the game and let everyone know we started it
			self._start_game()
			global_client_manager.game_condition.notify_all()
			# Release the run lock
			global_client_manager.game_condition.release()
		else:
			print "Game is still not full, waiting on more players"
			# Spin waiting for the server to fill up. This releases the
			# run lock and waits for the game to start
			global_client_manager.game_condition.wait()
			global_client_manager.game_condition.release()

		# TODO: Game has started, add any info given in start
		self.respond(200, reply)

	def _validate_client(self, json):
		"""Validate a client's request to proceed.

		Checks with the client manager that a client is who they say they are.
		Kicks anyone out who doesn't meet the bouncer's minimum requirements.
		"""

		client_id = json['id']
		token = json['auth']
		if global_client_manager.auth.authorize_client(client_id, token):
			return True
		else:
			# Bad call to client, bail us out
			self.respond(401, {'error': 'Bad id or auth code'})
			return False

	def _start_game(self):
		init_game(global_client_manager)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""A basic threaded HTTP server."""

	# Inheriting from ThreadingMixIn automatically gives us the default
	# functions we need for a threaded server.
	pass
