#!/usr/bin/env python

from mm18.game.engine import Engine

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

def init_game():
	"""Start up the game"""
	global _engine
	_engine = Engine()

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

	"""Get the status of the player, don't return anything
	that shouldn't be visible to the player

	JSON Input Expectations:
		id - Request player's ID
		auth - Request player's authentication token

	JSON Output Expectations:
		error - Error message if any
		health - Request player's base health
		resources - The request player's resources
		
	"""

	pass

def board_get(regex, **json):
	
	"""Get the player's board status

	JSON Input Expectations:
		id - Request player's ID
		auth - Request player's authentication token



	JSON Output Expectations:
		error - Error message if any
		towers - The list of all towers to be further
			parsed by the game clients
		units - The list of all units on the board
			to be further parsed by the game clients
	"""

	pass

def tower_upgrade(regex, **json):
	"""Upgrade a certain tower, if possible

	JSON Input Expectations:
		id - Request player's ID
		auth - Request player's authentication token

	JSON Output Expectations:
		error - Error message if any
		tower - The tower that was upgraded (or just the unupgraded
			one if the update failed)
		resources - The player's updated resources
		
	"""

	pass

def tower_specialize(regex, **json):

	"""Specialize a certain tower, if possible

	JSON Input Expectations:
		id - Request player's ID
		auth - Request player's authentication token

	JSON Output Expectations:
		error - Error message if any
		tower - The tower that was upgraded (or just the unupgraded
			one if the update failed)
		resources - The player's updated resources
		
	"""


	pass

def tower_sell(regex, **json):

	"""

	JSON Input Expectations:
		id - Request player's ID
		auth - Request player's authentication token

	JSON Output Expectations:
		error - Error message if any
		resources - Your updated resource count

	"""


	pass


def tower_get(regex, **json):
	
	"""

	JSON Input Expectations:
		id - Request player's ID
		auth - Request player's authentication token


	JSON Output Expectations:
		error - Error message if any
		tower - The requested tower (none if it doesn't exist)

	"""

	pass


def tower_create(regex, **json):
	
	"""

	JSON Input Expectations:
		id - Request player's ID
		auth - Request player's authentication token
		position - A tuple for the new tower's position

	JSON Output Expectations:
		error - Error message if any
		tower - The new tower, or none if it failed
		resources - The updated player's resources
	"""

	pass


def tower_list(regex, **json):
	
	"""

	JSON Input Expectations:
		id - Request player's ID
		auth - Request player's authentication token


	JSON Output Expectations:
		error - Error message if any
		towers - The list of towers on the board
	"""

	pass

def unit_status(regex, **json):
	
	"""

	JSON Input Expectations:
		id - Request player's ID
		auth - Request player's authentication token
		

	JSON Output Expectations:
		error - Error message if any
		unit - The unit (or none if something went wrong)

	"""

	pass

def unit_create(regex, **json):
	
	"""

	JSON Input Expectations:
		id - Request player's ID
		auth - Request player's authentication token


	JSON Output Expectations:
		error - Error message if any
		unit - The unit (or none if something went wrong)
	"""

	pass
