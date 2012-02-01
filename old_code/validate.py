#!/usr/bin/env python
import unittest
from numbers import Number
from game_instance import game
from vector import distance
import Constants
import traceback

def extract(keys, dict):
	answer = {}
	for k in keys:
		answer[k] = dict[k]
	return answer

resource_counter = 0

def handle_input(input, turn):
	"""Handle POST request data and passes to validators.

	@param input: Dictionary of input values to handle
	"""
	if 'auth' in input.keys():
		alive_players = [x.auth for x in game.players.itervalues() if x.alive]
		if input['auth'] in alive_players:
			player = game.get_player_by_auth(input['auth'])
			return validate_actions(game.players[id(player)], input, turn)
		else:
			return {'success':False, 
					'message':'bad auth token or non-active player'}
	else:
		return {'success':False, 'message':'no auth token provided'}

def validate_actions(player, input, turn):
	"""Validate actions requested by a player
False
	@param player: The player requesting these actions
	@param input: JSON actions to parse
	@return JSON dump of parse results
	""" 
	
	if 'actions' not in input:
		return {'success':False, 'message': 'no actions provided'}
	results = []
	with game.action_list_lock:
		game.actions[turn][player.auth] = []

	resource_counter = player.resources
	player.missed = 0
	for action in input['actions']:
		try:
			if action['obj_type'] == "Ship":
				results.append(validate_ship_action(action, player, turn, resource_counter))
			elif action['obj_type'] == "Base":
				results.append(validate_base_action(action, player, turn, resource_counter))
			elif action['obj_type'] == "Refinery":
				results.append(validate_refinery_action(action, player, turn, resource_counter))
			elif action['obj_type'] == "Player":
				results.append(validate_player_action(action, player, turn, resource_counter))
			else:
				results.append({'success':False, 'message':'bad or no obj_type in action'})
		except Exception as e:
			print e.__class__
			traceback.print_exc()
			results.append({'success':False, 'message':'action caused server error'})
	with game.action_list_lock:
		game.completed_turns[game.turn][player.auth] = True
	return results

def validate_ship_action(action, player, turn, resource_counter):
	"""Valide an action performed by a ship

	@param action: Action to validate
	@param player: The player that requested the action
	"""
	# make sure a ship action has all required keys
	attrs = ['command', 'obj_id', 'args']
	for attr in attrs:
		if attr not in action.keys():
			return {'success':False, 
					'message':'ship action requires a %s attribute' % attr}

	# attempt to coerce the obj_id to int
	try:
		obj_id = action['obj_id']
	except:
		return {'success':False, 'message':'invalid ship id'}

	# check if ship exiss
	if obj_id in game.game_map.ships.keys():
		ship = game.game_map.ships[obj_id]
	else:
		return {'success':False, 'message': 'ship does not exist'}

	# make sure the player owns the ship
	if ship.owner != player:
		return {'success':False, 'message':'not authenticated for that ship'}

	# make sure args is a dict
	if not isinstance(action['args'], dict):
		return {'success':False, 'message':'args must be a object'}

	# validate commands
	if action['command'] == 'thrust':
		if ship.methods_used['thrust']:
			return {'success':False, 'message':'thrust action already used'}
		elif 'direction' not in action['args'].keys():
			return {'success':False, 'message':'thrust requires direction arg'}
		elif not isinstance(action['args']['direction'], list):
			return {'success':False, 'message':'direction must be list'}	
		elif 'speed' not in action['args'].keys():
			return {'success':False, 'message':'thrust requires speed arg'}
		elif not isinstance(action['args']['speed'], Number):
			return {'success':False, 'message':'speed must be Number'}
		else:
			accel = action['args']['direction']
			try:
				(a, b) = (accel[0], accel[1])
			except:
				return {'success':False, 'message':'invalid direction values'}
			result = {'object': ship,
					  'method': action['command'],
					  'params': extract(['direction', 'speed'], action['args'])}
			with game.action_list_lock:
				game.actions[turn][player.auth].append(result)
			ship.methods_used['thrust'] = True
			return {'success' : True, 'message':'success'}

	elif action['command'] == 'fire':
		if ship.methods_used['fire']:
			return {'success':False, 'message':'fire action already used'}
		elif 'direction' not in action['args'].keys():
			return {'success':False, 'message':'fire requires direction arg'}
		else:
			direction = action['args']['direction']
			if not isinstance(direction, list):
				return {'success':False, 'message':'direction must be a list'}
			result = {'object': ship,
					  'method': action['command'],
					  'params':  extract(['direction'], action['args'])}
			with game.action_list_lock:
				game.actions[turn][player.auth].append(result)
			ship.methods_used['fire'] = True
			return {'success' : True, 'message':'success'}

	elif action['command'] == 'create_refinery':
		if ship.methods_used['create_refinery']:
			return {'success':False, 'message':'create_refinery action already used'}
		elif resource_counter - Constants.refinery_price < 0:
			return {'success':False, 
					'message':'not enough resources'}
		elif 'asteroid_id' not in action['args'].keys():
			return {'success':False, 
					'message':'create_refinery requires asteroid_id arg'}
		elif player.resources < Constants.refinery_price:
			return {'success':False, 'message':'not enough resources!'}
		else:
			asteroid_id = action['args']['asteroid_id']
			if not isinstance(asteroid_id, int):
				return {'success':False, 'message':'asteroid_id must be int'}
			asteroid = game.game_map.asteroids[asteroid_id]
			if distance(ship.position, asteroid.position) > \
					Constants.ship_build_radius:
				return {'success':False, 'message':'too far away from asteroid'}
			if asteroid.refinery != None:
				return {'success':False, 'message':'asteroid already has a refinery'}
			result = {'object': ship,
					  'method': action['command'],
					  'params': extract(['asteroid_id'], action['args'])}
			# TODO Check if another ship has built a base/refinery
			with game.action_list_lock:
				game.actions[turn][player.auth].append(result)
			ship.methods_used['create_refinery'] = True
			resource_counter -= Constants.refinery_price
			return {'success' : True, 'message':'success'}

	elif action['command'] == 'create_base':
		if ship.methods_used['create_base']:
			return {'success':False, 
					'message':'create_base action already used'}
		elif turn == 0:
			return {'success':False, 
					'message':'create_base action can\'t be used first turn'}
		elif resource_counter - Constants.base_price < 0:
			return {'success':False, 
					'message':'not enough resources'}
		elif 'planet_id' not in action['args'].keys():
			return {'success':False, 
					'message':'create_base requires planet_id arg'}
		else:
			planet_id = action['args']['planet_id']
			if not isinstance(planet_id, int):
				return {'success':False, 'message':'planet must be int'}
			planet = game.game_map.planets[planet_id]
			if distance(ship.position, planet.position) > \
					Constants.ship_build_radius:
				return {'success':False, 'message':'too far away from planet'}
			if planet.base != None:
				return {'success':False, 'message':'planet already has a base'}
			result = {'object': ship,
					  'method': action['command'],
					  'params': extract(['planet_id'], action['args'])}
			with game.action_list_lock:
				game.actions[turn][player.auth].append(result)
			ship.methods_used['create_base'] = True
			resource_counter -= Constants.base_price
			return {'success' : True, 'message':'success'}

	else:
		return {'success':False, 'message':'invalid ship command'}

def validate_base_action(action, player, turn, resource_counter):
	"""
	Validate an action performed by a base

	@param action: Action to validate
	@param player: The player that requested the action
	"""
	# make sure a base action h as all required keys
	attrs = ['command', 'obj_id', 'args']
	for attr in attrs:
		if attr not in action.keys():
			return {'success':False, 
					'message':'base action requires a %s attribute' % attr}

	# attempt to coerce the obj_id to int
	try:
		obj_id = action['obj_id']
	except:
		return {'success':False, 'message':'invalid base id'}

	# check if base exists
	base = None
	for planet in game.game_map.planets.itervalues():
		if obj_id == id(planet.base):
			base = planet.base
	if base == None:
		return {'success':False, 'message': 'base does not exist'}

	# make sure the player owns the base
	if base.owner != player:
		return {'success':False, 'message':'not authenticated for that base'}

	# check to see if base is active
	if base.built > 0:
		return {'success':False, 'message':'base is under construction'}

	# check if the base is busy
	if base.busy != 0:
		return {'success':False, 'message':'base is busy'}

	# make sure args is a dict
	if not isinstance(action['args'], dict):
		return {'success':False, 'message':'args must be a object'}

	if action['command'] == 'create_ship':
		if 'position' not in action['args'].keys():
			return {'success':False, 
					'message':'create_ship requires position arg'}
		elif not isinstance(action['args']['position'], list):
			return {'success':False, 'message':'position must be list'}
		elif resource_counter - Constants.ship_price < 0:
			return {'success':False, 
					'message':'not enough resources'}
		position = action['args']['position']
		if distance(position, base.position) > \
				Constants.base_build_radius:
			return {'success':False, 
					'message':'too far away to build ship'}
		else:
			position = action['args']['position']
			try:
				(a, b) = (position[0], position[1])
			except:
				return {'success':False, 'message':'invalid position values'}
			result = {'object': base,
					  'method': action['command'],
					  'params':extract(['position'], action['args']) }
			with game.action_list_lock:
				game.actions[turn][player.auth].append(result)
			base.busy = Constants.base_build_busy
			resource_counter -= Constants.ship_price
			return {'success' : True, 'message':'success'}

	elif action['command'] == 'salvage_ship':
		if 'ship_id' not in action['args'].keys():
			return {'success':False, 'message':'salvage_ship requires ship_id arg'}
		else:
			ship_id = action['args']['ship_id']
			if not isinstance(ship_id, int):
				return {'success':False, 'message':'ship must be int'}
			ship = game.game_map.ships[ship_id]
			if distance(ship.position, base.position) > \
					Constants.base_salvage_radius:
				return {'success':False, 
						'message':'too far away to salvage ship'}
			result = {'object': base,
					  'method': action['command'],
					  'params': extract(['ship_id'], action['args'])}
			with game.action_list_lock:
				game.actions[turn][player.auth].append(result)
			base.busy = Constants.base_salvage_busy
			return {'success' : True, 'message':'success'}

	elif action['command'] == 'repair_ship':
		if 'ship_id' not in action['args'].keys():
			return {'success':False, 'message':'repair_ship requires ship_id arg'}
		else:
			ship_id = action['args']['ship_id']
			if not isinstance(ship_id, int):
				return {'success':False, 'message':'ship must be int'}
			ship = game.game_map.ships[ship_id]
			if distance(ship.position, base.position) > \
					Constants.base_repair_radius:
				return {'success':False, 
						'message':'too far away to repair ship'}
			elif ship.health == Constants.base_health:
				return {'success':False, 
						'message':'ship already at full health'}
			result = {'object': base,
					  'method': action['command'],
					  'params': extract(['ship_id'], action['args'])}
  			with game.action_list_lock:
				game.actions[turn][player.auth].append(result)
			base.busy = Constants.base_repair_busy
			return {'success' : True, 'message':'success'}
 
	elif action['command'] == 'destroy':
		result = {'object': base,
				  'method': action['command'],
				  'params': {}}
		with game.action_list_lock:
			game.actions[turn][player.auth].append(result)
		return {'success' : True, 'message':'success'}

	else:
		return {'success':False, 'message':'invalid base command'}

def validate_refinery_action(action, player, turn, resource_counter):
	"""
	Validate an action performed by a refinery

	@param action: Action to validate
	@param player: The player that requested the action
	"""
	# make sure a refinery action has all required keys
	attrs = ['command', 'obj_id', 'args']
	for attr in attrs:
		if attr not in action.keys():
			return {'success':False, 
					'message':'refinery action requires a %s attribute' % attr}

	# attempt to coerce the obj_id to int
	try:
		obj_id = action['obj_id']
	except:
		return {'success':False, 'message':'invalid refinery id'}

	# check if refinery exists
	for asteroid in game.game_map.asteroids.itervalues():
		if obj_id == id(asteroid.refinery):
			refinery = asteroid.refinery
	else:
		return {'success':False, 'message': 'refinery does not exist'}

	# make sure the player owns the base
	if refinery.owner != player:
		return {'success':False, 'message':'not authenticated for that refinery'}

	# check to see if base is active
	if refinery.built > 0:
		return {'success':False, 'message':'refinery is under construction'}

	# make sure args is a dict
	if not isinstance(action['args'], dict):
		return {'success':False, 'message':'args must be a object'}

	if action['command'] == 'destroy':
		result = {'object': refinery,
				  'method': action['command'],
				  'params': {}}
		with game.action_list_lock:
			game.actions[turn][player.auth].append(result)
		return {'success' : True, 'message':'success'}
	
	else:
		return {'success':False, 'message':'invalid refinery command'}
	
def validate_player_action(action, player, turn):
	"""
	Validate an action performed by a player

	@param action: Action to validate
	@param player: The player that requested the action
	"""
	# make sure a base action has all required keys
	attrs = ['command']
	for attr in attrs:
		if attr not in action.keys():
			return {'success':False, 
					'message':'player action requires a %s attribute' % attr}

	if action['command'] == 'forfeit':
		if player.alive == False:
			return {'success' : False, 'message':'player not active'}
		else:
			game._log("Player " + player.name + " foreited the game.")
			result = {'object': player,
					  'method': action['command'],
					  'params': {}}
			with game.action_list_lock:
				game.actions[turn][player.auth].append(result)
			return {'success' : True, 
					'message':'success, thanks for playing!'}
	else:
		return {'success':False, 'message':'invalid base command'}




class UnitTests(unittest.TestCase):
	def test_main(self):
		print "hello world"
		self.assertTrue(True)

if __name__ == "__main__":
	unittest.main()
