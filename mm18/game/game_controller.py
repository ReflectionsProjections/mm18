#!/usr/bin/env python

from mm18.game.engine import Engine
## @file game_controller.py

# A global variable stores the active game engine
_engine = None

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

# Setup functions

def require_running_game(func):
	def check_run_and_process(regex, **json):
		if _engine is None:
			print "No engine"
			# Game isn't running, call error handling
			return respond_for_no_game()
		elif not is_running():
			print "Game not running"
			return respond_for_done_game()
		else:
			try:
				return func(regex, **json)
			except KeyError:
				return missing_data()

	return check_run_and_process

def init_game(client_manager, game_log):
	global _engine
	_engine = Engine.spawn_game(client_manager.clients, game_log)

def respond_for_no_game():
	output = (404, {'error': "Game is not yet running"})
	return output

def respond_for_done_game():
	output = (404, {'error': "Game has ended"})
	return output

def missing_data():
	output = (400, {'error': "Valid JSON but missing required input keys"})
	return output

def game_running():
	if _engine:
		return _engine.running
	else:
		return False

## Engine API hooks

## Get the status of the currently running game.
#  @param **json Expected to contain "Request player's ID" (id) and "Request player's authentication token" (auth)
#  @return a tuple containing the return code and JSON containing "Error message if any" (error) and "List of tuples player ids and their base's health" (players)
@require_running_game
def get_game_status(regex, **json):

	"""Get the status of the currently running game

	JSON Input Expectations:
		id - Request player's ID
		auth - Request player's authentication token

	JSON Output Expectations:

	"""
	ids = _engine.get_player_ids()
	playerList = []
	for player_id in ids:
		playerHealth = _engine.get_player(player_id).healthIs()
		currPlayer = (player_id, playerHealth)
		playerList.append(currPlayer)

	code = 200;

	jsonret = {"players": playerList}

	return (code, jsonret)

## Get the status of the player, don't return anything
#  that shouldn't be visible to the player
#  @param **json Expected to contain "Request player's ID" (id) and "Request player's authentication token" (auth)
#  @return a tuple containing the return code and JSON containing "Error message if any" (error), "Request player's base health" (health)
@require_running_game
def get_player_status(regex, **json):

	playerID = json["id"]
	playerRequested = regex[1]

	player = _engine.get_player(playerRequested)

	playerHealth = -1
	playerResources = -1
	playerLevel = -1

	if(player != None):
		playerHealth = player.healthIs()
		if(playerRequested == playerID):
			playerResources = player.resourcesIs()
			playerLevel = player.allowedUpgradeIs()

	code = 200
	error = ""
	
	if player == None :
		code = 409
		error = "Invalid player ID"

	jsonret = {"error": error, "health" : playerHealth,
			"resources" : playerResources, "level" : playerLevel}

	return (code, jsonret)
	

## Get the player's board status
#  @param **json Expected to contain "Request player's ID" (id) and "Request player's authentication token (auth)
#  @return  a tuple containing the return code and JSON containing "Error message if any" (error), "The list of all towers to be further parsed by the game clients" (towers), and "The list of all units on the board to be further parsed by the game clients" (units)
@require_running_game
def board_get(regex, **json):

	playerid = regex[1]

	board = _engine.board_get(playerid)
	
	towers = []
	units = []
	
	code = 409
	board = "Invalid player ID"

	if board != None :
		unitsDict = board.unitList

		for elem in board.tower:
			towerCoords = elem
			towerID = board.tower[elem].ID
			towerTuple = (towerID, towerCoords)
			towers.append(towerTuple)

		for elem in board.unitList:
			unit, unitCoord = elem
			unitTuple = (unit.owner, unitCoord, unit.level, 
					unit.specialisation, unit.health)
			units.append(unitTuple)

		code = 200
		error = ""

	jsonret = {"error": error, "towers": towers, "units": units}
	

	return (code, jsonret)

## Upgrade a certain tower, if possible
#  @param **json Expected to contain "Request player's ID" (id) and "Request player's authentication token" (auth)
#  @return  a tuple containing the return code and JSON containing "Error message if any" (error), "The tower that was upgraded (or just the unupgraded one if the update failed)" (tower), and "The player's updated resources" (resources)
@require_running_game
def tower_upgrade(regex, **json):
	tower = _engine.tower_upgrade(regex[1], json["id"])
	player = _engine.get_player(json["id"])
	code = 200
	error = ""
	resources = player.resourcesIs()
	
	if(tower == None):
		towerID = -1
		towerSpec = -1
		towerUpgrade = -1
		code = 409
		error = "Insufficient funds"
	else:
		towerID = tower.ID
		towerSpec = tower.specialisation
		towerUpgrade = tower.upgrade

	jsonret = {"error": error, "towerID": towerID, 
		"towerSpec": towerSpec, "towerUpgrade": towerUpgrade, 
			"resources": resources}

	return (code, jsonret)


## Specialize a certain tower, if possible
#  @param **json Expected to contain "Request player's ID" (id) and "Request palyer's authentication token" (auth)
#  @return  a tuple containing the return code and JSON containing "Error message if any" (error), "The tower that was upgraded (or just the unupgraded one if the update failed)" (tower), and "The player's updated resources" (resources)
@require_running_game
def tower_specialize(regex, **json):
	tower = _engine.tower_specialize(regex[1], json["id"])
	player = _engine.get_player(json["id"])
	code = 200
	error = ""
	resources = player.resourcesIs()
	

	if(tower == None):
		towerID = -1
		towerSpec = -1
		towerUpgrade = -1
		code = 409
		error = "Insufficient funds"
	else:
		towerID = tower.ID
		towerSpec = tower.specialisation
		towerUpgrade = tower.upgrade


	jsonret = {"error": error, "towerID": towerID, 
		"towerSpec": towerSpec, "towerUpgrade": towerUpgrade, 
			"resources": resources}

	return (code, jsonret)


## 
# @param **json Expected to contain "Request player's ID" (id) and "Request player's authentication token" (auth)
# @return  a tuple containing the return code and JSON containing "Error message if any" (error) and "Your updated resources count" (resources)
@require_running_game
def tower_sell(regex, **json):
	playerID = regex[1]
	playerAuth = json["id"]
	notOwner = 0
	if(playerID == playerAuth):
		playerAfter = _engine.tower_sell(regex[1], json["id"])
	else:
		error = "You are not the owner of this tower"
		notOwner = 1

	code = 200
	error = ""

	if notOwner == 0 and json["id"].resourcesIs() == playerAfter.resourcesIs() :
		code = 409
		error = "Invalid tower"


	jsonret = {"error": error, "resources": afterPlayer.resourcesIs()}

	return (code, jsonret)
	

## 
# @param **json Expected to contain "Request player's ID" (id) and "Request player's authentication token" (auth)
# @return  a tuple containing the return code and JSON containing "Error message if any" (error) and "The requested tower (none if it doesn't exist)" (tower)
@require_running_game
def tower_get(regex, **json):
	tower = tower_get(regex[1], json["id"])
	
	code = 200
	error = ""
	towerID = -1
	towerSpec = -1
	towerUpgrade = -1

	if tower == None:
		code = 409
		error = "Tower not visible or invalid tower ID"
	else:
		towerID = tower.ID
		towerSpec = tower.specialisation
		towerUpgrade = tower.upgrade


	jsonret = {"error": error, "towerID": towerID, 
		"towerSpec": towerSpec, "towerUpgrade": towerUpgrade, 
			"resources": resources}


	return (code, jsonret)


## 
# @param **json Expected to contain "Request player's ID" (id), "Request player's authentication token" (auth), "A tuple for the new tower's position" (position), "level of the new tower" (level), and "specification of the new tower" (spec)
# @return  a tuple containing the return code and JSON containing "Error message if any" (error), "The new tower, or none if it failed" (tower), and "The updated player's resources" (resources)
@require_running_game
def tower_create(regex, **json):
	tower = _engine.tower_create(json["id"], json["position"], json["level"], json["spec"])
	
	code = 200
	error = ""
	towerID = -1
	towerSpec = -1
	towerUpgrade = -1

	if tower == None:
		code = 409
		error = "Tower not visible or invalid tower ID"
	else:
		towerID = tower.ID
		towerSpec = tower.specialisation
		towerUpgrade = tower.upgrade


	jsonret = {"error": error, "towerID": towerID, 
		"towerSpec": towerSpec, "towerUpgrade": towerUpgrade, 
			"resources": resources}


	return (code, jsonret)

## 
# @param **json Expected to contain "Request player's ID" (id), "Request player's authentication token" (auth), "The unit level" (level), "The unit specialization" (spec), "The target player's id" (target_id), "The path of the enemy board to go on" (path) 
# @return  a tuple containing the return code and JSON containing "Error message if any" (error) and "The unit (or none if something went wrong)" (unit)
@require_running_game
def unit_create(regex, **json):
	
	unit = _engine.unit_create(json["id"], json["level"], json["spec"],
			json["target_id"], json["path"])
	
	code = 200
	error = ""
	unitID = -1
	unitLevel = -1
	unitSpec = -1
	unitTargetID = -1
	unitPath = -1

	if(unit == None):
		code = 409
		error = "Invalid player ID, or invalid unit specification"
	else:
		unitID = json["id"]
		unitLevel = json["level"]
		unitTargetID = json["target_id"]
		unitSpec = json["spec"]
		unitPath = json["path"]

	jsonret = {"error": error, "playerID": unitID, "unitLevel": unitLevel,
			"playerTargetID": unitTargetID, "unitSpec": unitSpec, "unitPath": unitPath}

	return (code, jsonret)
