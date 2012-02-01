#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 noexpandtab

from encodings import aliases
from encodings import hex_codec
import os
import sys
import optparse
import json
import unittest
import time
import thread
import signal

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
from urlparse import urlparse
from urlparse import parse_qs

import Constants

from validate import handle_input

from game_instance import game, game_map

class MMHandler(BaseHTTPRequestHandler):
	"""
	Server request handler for Mechmania 17.
	"""

	# URI Handling Functions

	def log_message(self,  *args, **kwargs):
		pass

	def game_status(self, params):
		"""
		Handle a request for the game state. Write out to the request
		handler json data with active players and whether or not the game
		has started.

		@type  params: parsed URL query paramater dictionary
		@param params: URL paramater string. No required fields for function
				to operate.
		"""

		gameStatus = game.game_status()
		self.respond()
		self.wfile.write(json.dumps(gameStatus))

	def game_avail_info(self, params):
		"""
		Handle a request for the game state. Write out json data with
		all information available to the player.

		@type  params: parsed URL query paramater dictionary
		@param params: URL paramater string. Must contain 'auth' field
				with valid user authentication id.
		"""

		gameStatus = game.game_avail_info(params['auth'][0])
		self.respond()
		self.wfile.write(json.dumps(gameStatus))

	def viz(self, params):
		"""
		Display the visualizer
		"""
		parsedURL = urlparse(self.path)
		xpath = parsedURL.path.replace("/viz/","./visualizer/")
		xpath = xpath.replace("..",".")
		f = open(xpath)
		if f:
			self.send_response(200)
			self.end_headers()
			self.wfile.write(f.read())
		else:
			self.send_error(404, "Vad visualizer file path")


	def game_visualizer(self, params):
		"""
		Handle a request by the visualizer to get all objects.  Write out
		all object data to json.information on the last turn

		@type  params: parsed URL query paramater dictionary
		@param params: URL paramater string. Must contain 'auth' field
				with valid user authentication id.
		"""
		gameStatus = game.game_visualizer(params['auth'][0])
		self.respond()
		self.wfile.write(json.dumps(gameStatus))

	def game_turn_get(self, params):
		"""
		Handle a request for the last completed turn. Writes out json
		containing the number of the next game turn.

		@type  params: parsed URL query paramater dictionary
		@param params: URL paramater string. No required fields for function
				to operate.
		"""
		self.respond()
		output = json.dumps(game.turn_number())
		self.wfile.write(output)

	def game_turn_wait(self, params):
		game.wait_for_next(params['turn'][0])
		self.respond()
		output = json.dumps(game.turn_number())
		self.wfile.write(output)

	def game_turn_post(self, input):
		"""
		Handle a POST request for the next turn. Writes out the json
		containing success status for each requested action.

		@type  input: parsed URL query paramater dictionary
		@param input: JSON dictionary with the actions to be performed
				on this turn for the current user. Must contain a valid
				player authentication token.
		"""
		parsedURL = urlparse(self.path)
		requested_turn = int(self.explode_path(parsedURL)[-2])
		if requested_turn != game.turn:
			output = {"success":False, 
					  "message":"must request current turn"}
		else:
			output = handle_input(input, requested_turn)

		self.respond()
		output = json.dumps(output)
		self.wfile.write(output)

	def game_constants(self, params):
		self.respond()
		self.wfile.write(json.dumps(Constants.to_dict()))

	def game_join(self, params):
		"""
		Handle a request to join the game. Writes out json data with the
		name and authentication token of the player if join succeeds or
		returns HTTP 400 error on join failure.

		@type  params: parsed URL query paramater dictionary
		@param params: URL paramater string. Requires a valid player
				name and an authentication token to work.
		"""

		if 'auth' not in params or 'name' not in params:
			self.send_error(400, "Auth code or name not provided")
			return

		authCode = params['auth'][0]
		name = params['name'][0]

		successObj = game.add_player(name, authCode)
		self.respond()
		self.wfile.write(json.dumps(successObj))

	# These map URIs to handlers depending on request method
	GET_PATHS = {
		'viz': viz,
		'game': {
			'constants': game_constants,
			'info': {
				'': game_status,
				'all':game_avail_info,
				'visualizer':game_visualizer,
				},
			'turn': game_turn_get,
			'wait': game_turn_wait,
			'join': game_join,
		},
	}

	POST_PATHS = {
		'game': {
			'turn': game_turn_post,
		},
	}

	# Other helper functions

	def explode_path(self, parsedURL):
		"""
		Seperate a URL path into subcomponents for each directory.

		@type  parsedURL: parsed URL path
		@param parsedURL: The path to be seperated.

		@rtype: list
		@return: A list of all the directories in the path.
		"""

		exploded_path = parsedURL.path[1:].split('/')
		search_paths = []

		if exploded_path[0] == '':
			self.send_error(403, "Requests to the root are invalid.\
					Did you mean /game/turn?")
			return

		for path in exploded_path:
			if path is not '':
				search_paths.append(path)

		search_paths.append('')
		return search_paths


	def walk_path(self, search_dict, search_path):
		"""
		Walk the PATHS object to find the correct handler based on the
		URL query sent.

		@type  search_dict: dictionary
		@param search_dict: Dictionary of different request handlers.

		@type  search_path: list
		@param search_path: Exploded URL list of path components.

		@rtype: function
		@return: The server class function that should be used as the
				handler for the given URL request.
		"""

		first_item = search_path.pop(0)
		if first_item in search_dict:
			if isinstance(search_dict[first_item], dict):
				return self.walk_path(search_dict[first_item], \
						search_path)
			else:
				return search_dict[first_item]
		else:
			return None

	def send_error(self, code, text):
		"""
		Send out an error to the requestor using JSON.

		@type  code: int
		@param code: HTTP/1.1 status code to send out.

		@type  text: string
		@param text: Error message to send out.
		"""

		# send_error doesn't do JSON responses; we
		# want json, so here's our own error thing
		self.send_response(code)
		self.send_header('Content-type', 'application/json')
		self.end_headers()
		self.wfile.write(json.dumps({'error': text}))

	def respond(self):
		"""
		Send out an HTTP 200 (OK status) and JSON content-type header.
		"""
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()

	# HTTP Request Handlers

	def do_GET(self):
		"""
		Process a client's GET request, parsing the URL and passing data
		to the appropriate handler method, and writing JSON data out.
		"""
		parsedURL = urlparse(self.path)
		params = parse_qs(parsedURL.query)

		search_paths = self.explode_path(parsedURL)
		handler = self.walk_path(self.GET_PATHS, search_paths)
		if handler is not None:
			handler(self, params)
		else:
			self.send_error(404, "Unknown resource identifier: %s" % self.path)


	def do_POST(self):
		"""
		Process a client's POST request, parsing URL and passing data to
		appropriate handler methods, and writing JSON data out.
		"""
		length = int(self.headers.getheader('content-length'))
		rfile = self.rfile.read(length)
		try:
			input = json.loads(rfile)
		except ValueError:
			self.send_error(400, "Bad JSON.")
			return
		parsedURL = urlparse(self.path)
		search_paths = self.explode_path(parsedURL)
		handler = self.walk_path(self.POST_PATHS, search_paths)
		if handler is not None:
			handler(self, input)
		else:
			self.send_error(404, "Unknown resource identifier: %s"\
					% self.path)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer): pass

def start_timeout(game):
	time.sleep(5)
	if not game.active:
		if len(game.players) == 0:
			print "No players"
			os.kill(os.getpid(), signal.SIGQUIT)
		else:
			print "Starting with less players"
			game_map.max_players = len(game.players)
			game._begin()
	else:
		return

def Main():
	argsys = optparse.OptionParser(description="Mechmania 17 Main Server")
	argsys.add_option('-p', '--port', metavar='PORT', nargs=1, type='int',
			default=7000, dest='port', help='Port to listen on')
	argsys.add_option('-n', '--num-players', metavar='PLAYERNUM', nargs=1,
			type='int', default=2, dest='num_players',
			help='Number of players who will join the game')
	argsys.add_option('--unit-tests', action='store_true',
			help='Run unit tests', dest='unittest', default=False)
	(opts, args) = argsys.parse_args()
	if opts.unittest:
		# Reset the arguments so that only filename is passed
		sys.argv = sys.argv[:1]
		unittest.main()

	# Set up the game
	port = opts.port
	game_map.max_players = opts.num_players
	game.viz_auth = raw_input()
	for i in range(0,opts.num_players):
		game.allowed_auths.append(raw_input())


#	thread.start_new_thread(start_timeout, (game,))
	server = ThreadedHTTPServer(('', port), MMHandler)
	server.allow_reuse_address = True
	server.serve_forever()

if __name__ == '__main__':
	Main()
