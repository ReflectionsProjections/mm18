#!/usr/bin/env python

from mm18.game.engine import Engine
## @file game_controller.py

# A global variable stores the active game engine
_engine = None

# Setup functions

def init_game():
	"""Start up the game"""
## Runs the game and facilitates communication between the server, database,
#  and game logic.
#
#  Basic set of functions for facilitating communication between the server, game
#  storage, and logic/rules of the game.
#
#  Most functions in this file take arguments in the form (regex, **json)
#  where regex is the parsed regular expression match object (contains things
#  grabbed from the regular expression), and json is all the keyworded
#  arguments parsed out of the json sent to the server.
#
#  All functions with (regex, **json) input return a tuple in the form (code,
#  json), where code is the HTTP status code to respond with, and json is the
#  response dictionary to serialize and send out to the client.
#
#  The engine must be set with the initalizer before any of these functions will
#  work succesfully.

## Setup functions
def init_controller(gameEngine):
	global _engine
	_engine = Engine()

## Engine API hooks

## Get the status of the currently running game.
#  @param **json Expected to contain "Request player's ID" (id) and "Request player's authentication token" (auth)
def get_game_status(regex, **json):

	"""Get the status of the currently running game

	JSON Input Expectations:
		id - Request player's ID
		auth - Request player's authentication token

	JSON Output Expectations:

	"""


	pass

## Get the status of the player, don't return anything
#  that shouldn't be visible to the player
#  @param **json Expected to contain "Request player's ID" (id) and "Request player's authentication token" (auth)
#  @return JSON containing "Error message if any" (error), "Request player's base health" (health), and "The request player's resources" (resources)
def get_player_status(regex, **json):
	pass

## Get the player's board status
#  @param **json Expected to contain "Request player's ID" (id) and "Request player's authentication token (auth)
#  @return JSON containing "Error message if any" (error), "The list of all towers to be further parsed by the game clients" (towers), and "The list of all units on the board to be further parsed by the game clients" (units)
def board_get(regex, **json):
	pass

## Upgrade a certain tower, if possible
#  @param **json Expected to contain "Request player's ID" (id) and "Request player's authentication token" (auth)
#  @return JSON containing "Error message if any" (error), "The tower that was upgraded (or just the unupgraded one if the update failed)" (tower), and "The player's updated resources" (resources)
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

	tower = _engine.tower_upgrade(regex[1], json["id"])
	player = _engine.get_player(json["id"])
	code = 200
	error = ""
	resources = player.resourcesIs()

	if(tower == None):
		code = 409
		error = "Insufficient funds"

	jsonret = {"error": error, "tower": tower, "resources": resources}

	return (code, jsonret)


## Specialize a certain tower, if possible
#  @param **json Expected to contain "Request player's ID" (id) and "Request palyer's authentication token" (auth)
#  @return JSON containing "Error message if any" (error), "The tower that was upgraded (or just the unupgraded one if the update failed)" (tower), and "The player's updated resources" (resources)
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

	tower_id = regex[1]

## 
# @param **json Expected to contain "Request player's ID" (id) and "Request player's authentication token" (auth)
# @return JSON containing "Error message if any" (error) and "Your updated resources count" (resources)
def tower_sell(regex, **json):

	"""

	JSON Input Expectations:
		id - Request player's ID
		auth - Request player's authentication token

	JSON Output Expectations:
		error - Error message if any
		resources - Your updated resource count

	"""

	tower_id = regex[1]


## 
# @param **json Expected to contain "Request player's ID" (id) and "Request player's authentication token" (auth)
# @return JSON containing "Error message if any" (error) and "The requested tower (none if it doesn't exist)" (tower)
def tower_get(regex, **json):
	
	"""

	JSON Input Expectations:
		id - Request player's ID
		auth - Request player's authentication token


	JSON Output Expectations:
		error - Error message if any
		tower - The requested tower (none if it doesn't exist)

	"""

	tower_id = regex[1]


## 
# @param **json Expected to contain "Request player's ID" (id), "Request player's authentication token" (auth), and "A tuple for the new tower's position" (position)
# @return JSON containing "Error message if any" (error), "The new tower, or none if it failed" (tower), and "The updated player's resources" (resources)
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



## 
# @param **json Expected to contain "Request player's ID" (id) and "Request player's authentication toekn" (auth)
# @return JSON containing "Error message if any" (error) and "The list of towers on the board" (towers)
def tower_list(regex, **json):
	pass

## 
# @param **json Expected to contain "Request player's ID" (id) and "Request player's authentication token" (auth)
# @return JSON containing "Error message if any" (error) and "The unit (or none if something went wrong)" (unit)
def unit_status(regex, **json):
	pass

## 
# @param **json Expected to contain "Request player's ID" (id) and "Request player's authentication token" (auth)
# @return JSON containing "Error message if any" (error) and "The unit (or none if something went wrong)" (unit)
def unit_create(regex, **json):
	pass
