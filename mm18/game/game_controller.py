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
#  @return a tuple containing the return code and JSON containing "Error message if any" (error) and "List of tuples player ids and their base's health" (players)
def get_game_status(regex, **json):

	"""Get the status of the currently running game

	JSON Input Expectations:
		id - Request player's ID
		auth - Request player's authentication token

	JSON Output Expectations:

	"""
	ids = _engine.get_player_ids()
	playerList = []
	for player in ids:
		playerHealth = _engine.get_player(player).healthIs()
		currPlayer = (player, playerHealth)
		playerList = append(currPlayer)

	code = 200;

	jsonret = {"error": error, "players": playerList}

	return (code, jsonret)
	
	
	

## Get the status of the player, don't return anything
#  that shouldn't be visible to the player
#  @param **json Expected to contain "Request player's ID" (id) and "Request player's authentication token" (auth)
#  @return a tuple containing the return code and JSON containing "Error message if any" (error), "Request player's base health" (health)
def get_player_status(regex, **json):

	playerid = regex[1]
	player = _engine.get_player(playerid)
	playerHealth = -1
	if(player != None):
		playerHealth = player.healthIs()

	code = 200
	error = ""
	
	if player == None :
		code = 409
		error = "Invalid player ID"

	playerTuple = (player, playerHealth)
	jsonret = {"error": error, "player" : playerTuple}

	return (code, playerTuple)
	

## Get the player's board status
#  @param **json Expected to contain "Request player's ID" (id) and "Request player's authentication token (auth)
#  @return  a tuple containing the return code and JSON containing "Error message if any" (error), "The list of all towers to be further parsed by the game clients" (towers), and "The list of all units on the board to be further parsed by the game clients" (units)
def board_get(regex, **json):

	playerid = regex[1]

	board = _engine.board_get(playerid)
	
	towers = None
	units = None
	
	code = 409
	board = "Invalid player ID"

	if board != None :
		towers = board.tower
		units = board.unitList
		code = 200
		error = ""

	jsonret = {"error": error, "towers": towers, "units": units}
		
	return (code, jsonret)

## Upgrade a certain tower, if possible
#  @param **json Expected to contain "Request player's ID" (id) and "Request player's authentication token" (auth)
#  @return  a tuple containing the return code and JSON containing "Error message if any" (error), "The tower that was upgraded (or just the unupgraded one if the update failed)" (tower), and "The player's updated resources" (resources)
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
#  @return  a tuple containing the return code and JSON containing "Error message if any" (error), "The tower that was upgraded (or just the unupgraded one if the update failed)" (tower), and "The player's updated resources" (resources)
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

	tower = _engine.tower_specialize(regex[1], json["id"])
	player = _engine.get_player(json["id"])
	code = 200
	error = ""
	resources = player.resourcesIs()

	if tower == None :
		code = 409
		error = "Insufficient funds"

	jsonret = {"error": error, "tower": tower, "resources": resources}

	return (code, jsonret)


## 
# @param **json Expected to contain "Request player's ID" (id) and "Request player's authentication token" (auth)
# @return  a tuple containing the return code and JSON containing "Error message if any" (error) and "Your updated resources count" (resources)
def tower_sell(regex, **json):

	"""

	JSON Input Expectations:
		id - Request player's ID
		auth - Request player's authentication token

	JSON Output Expectations:
		error - Error message if any
		resources - Your updated resource count

	"""

	playerAfter = _engine.tower_sell(regex[1], json["id"])

	code = 200
	error = ""

	if json["id"].resourcesIs() == playerAfter.resourcesIs() :
		code = 409
		error = "Invalid tower"


	jsonret = {"error": error, "resources": afterPlayer.resourcesIs()}

	return (code, jsonret)
	

## 
# @param **json Expected to contain "Request player's ID" (id) and "Request player's authentication token" (auth)
# @return  a tuple containing the return code and JSON containing "Error message if any" (error) and "The requested tower (none if it doesn't exist)" (tower)
def tower_get(regex, **json):
	
	"""

	JSON Input Expectations:
		id - Request player's ID
		auth - Request player's authentication token


	JSON Output Expectations:
		error - Error message if any
		tower - The requested tower (none if it doesn't exist)

	"""

	tower = tower_get(regex[1], json["id"])
	
	code = 200
	error = ""

	if tower == None : 
		code = 409
		error = "Tower not visible or invalid tower ID"

	jsonret = {"error": error, "tower": tower}

	return (code, jsonret)


## 
# @param **json Expected to contain "Request player's ID" (id), "Request player's authentication token" (auth), "A tuple for the new tower's position" (position), "level of the new tower" (level), and "specification of the new tower" (spec)
# @return  a tuple containing the return code and JSON containing "Error message if any" (error), "The new tower, or none if it failed" (tower), and "The updated player's resources" (resources)
def tower_create(regex, **json):
	
	"""

	JSON Input Expectations:
		id - Request player's ID
		auth - Request player's authentication token
		position - A tuple for the new tower's position
		level - level of new tower
		spec - specification of the new tower

	JSON Output Expectations:
		error - Error message if any
		tower - The new tower, or none if it failed
		resources - The updated player's resources
	"""

	tower = _engine.tower_get(json["id"], json["position"], json["level"], json["spec"])

	code = 200
	error = ""

	if tower == None:
		code = 409
		error = "Invalid tower attributes (position, level, or specification)"
	
	jsonret = {"error": error, "tower": tower}

	return (code, jsonret)



## 
# @param **json Expected to contain "Request player's ID" (id), "Request player's authentication token" (auth) and "Player ID of whos board to get (playerid)"
# @return  a tuple containing the return code and JSON containing "Error message if any" (error) and "The list of towers on the board" (towers)
def tower_list(regex, **json):

	board = _engine.board_get(json["playerid"])
	towers = None

	if board != None:
		towers = board.tower;

	code = 200
	error = ""

	if board == None or towers == None:
		code = 409
		error = "Invalid player ID"
	
	jsonret = {"error": error, "towers": towers}

	return (code, jsonret)
	

## 
# @param **json Expected to contain "Request player's ID" (id) and "Request player's authentication token" (auth)
# @return  a tuple containing the return code and JSON containing "Error message if any" (error) and "The units on the board (or none if something went wrong)" (units)
def unit_status(regex, **json):

	board = _engine.board_get(json["playerid"])
	units = None

	if board != None:
		units = board.units();

	code = 200
	error = ""

	if board == None or units == None:
		code = 409
		error = "Invalid player ID"
	
	jsonret = {"error": error, "units": units}

	return (code, jsonret)
	

## 
# @param **json Expected to contain "Request player's ID" (id), "Request player's authentication token" (auth), "The unit level" (level), "The unit specialization" (spec), "The target player's id" (target_id), "The path of the enemy board to go on" (path) 
# @return  a tuple containing the return code and JSON containing "Error message if any" (error) and "The unit (or none if something went wrong)" (unit)
def unit_create(regex, **json):
	
	unit = _engine.unit_create(json["id"], json["level"], json["spec"], json["target_id"], json["path"])
	
	code = 200
	error = ""

	if(unit == None):
		code = 409
		error = "Invalid player ID, or invalid unit specification"

	jsonret = {"error": error, "unit": unit}

	return (code, jsonret)	
