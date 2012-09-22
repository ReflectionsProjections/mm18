#!/usr/bin/env python

# A global variable stores the active game engine
_engine = None

"""Runs the game and facilitates communication between the server, database,
and game logic.

Basic set of functions for facilitating communication between the server, game
storage, and logic/rules of the game.

Most functions in this file take arguments in the form (regex, **json)
where regex is the parsed regular expression match object (contains things
grabbed from the regular expression), and json is all the keyworded
arguments parsed out of the json sent to the server.

All functions with (regex, **json) input return a tuple in the form (code,
json), where code is the HTTP status code to respond with, and json is the
response dictionary to serialize and send out to the client.

The engine must be set with the initalizer before any of these functions will
work succesfully.
"""

# Setup functions

def init_controller(gameEngine):
	global _engine
	_engine = gameEngine

# Engine API hooks

def get_game_status(regex, **json):
	"""Get the status of the currently running game

	JSON Input Expectations:
		id - Request player's ID
		auth - Request player's authentication token

	JSON Output Expectations:

	"""

	pass

def get_player_status(regex, **json):
	pass

def board_get(regex, **json):
	pass

def tower_upgrade(regex, **json):
	pass

def tower_specialize(regex, **json):
	pass

def tower_sell(regex, **json):
	pass

def tower_get(regex, **json):
	pass

def tower_create(regex, **json):
	pass

def tower_list(regex, **json):
	pass

def unit_status(regex, **json):
	pass

def unit_create(regex, **json):
	pass
