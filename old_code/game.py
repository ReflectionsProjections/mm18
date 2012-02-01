#! /usr/bin/env python

import time
import thread
import threading
import unittest
import os
import json
import signal

from datetime import datetime
from vector import jitter_tuple
import Constants

class Game(object):
	"""
	The main Game class runs the game. This class accumulates
	and applies orders, provides turn results, and logs data.

	The Game directly stores the log file, the set of players,
	a set of pending orders for each player, the current turn,
	and whether the game is in progress.

	Ship information is stored in the game map.

	The game contains the logic for deciding when to take
	a turn, and for resolving a turn.
	"""

	def __init__(self, game_map, log_file):
		"""
		Initialize the game object.

		@type  game_map: game_map object
		@param game_map: Map object for the game

		@type  log_file: string
		@param log_file: Path to log file. Existing file at this path
				will be overwritten.
		"""
		self.game_map = game_map
		self.allowed_auths = []
		self.viz_auth = ''
		self.players = {}
		self.last_alive = []
		self.log_file = open(log_file, 'w')
		# List of orders for each turn, dictionaries indexed by player
		self.action_list_lock = threading.Lock()
		with self.action_list_lock:
			self.actions = [{}]
			self.completed_turns = [{}]
		# Player results, indexed by players
		self.player_result_lock = threading.Lock()
		self.lasers_shot_lock = threading.Lock()
		self.turn_lock = threading.Lock()
		self.turn_condition = threading.Condition(self.turn_lock)
		with self.player_result_lock:
			self.player_results = {}
		self.turn = -1
		self.active = False
		self.lasers_shot = [[]]


	def _log(self, message):
		"""
		Log a single-line message. Formatted with a timestamp and a
		trailing newline.

		@type  message: string
		@param message: Message to write out to the log file
		"""
		text = "%s: %s\n" % (datetime.now(), message)

		self.log_file.write(text)

	def _begin(self):
		from game_map import map_maker
		"""
		Create starting units and start the game turn loop.
		"""
		map_maker(self.players)
		self.active = True
		self.completed_turns.append({})
		self.turn_condition.acquire()
		self.turn = 0
		self.start_time = time.time()
		self.turn_condition.notify()
		self.turn_condition.release()
		self.last_turn_time = time.time()
		self._log("Game started.")
		print "game started"
		thread.start_new_thread(self._main, ())

	def _end(self):
		"""
		Stop the game main loop.
		"""
		self._log("Game ended.")
		alive = [x for x in self.players.values() if x.alive]
		if len(alive) == 0:
			alive = self.last_alive
			max = alive[0]
			for x in alive:
				if x.score > max.score:
					max = x
			wins = {"winner":max.auth, "score":max.score}
		if len(alive) == 1:
			wins = {"winner":id(alive[0]),"score":alive[0].score}
		else:
			max = alive[0]
			for x in alive:
				if x.score > max.score:
					max = x
			wins = {"winner":max.auth, "score":max.score}
		print json.dumps(wins)
		self.active = False
		time.sleep(5)
		os.kill(os.getpid(), signal.SIGQUIT)


	def _resolve_turn(self):
		from ship import Ship
		"""
		Apply all the orders which have been recieved for this turn,
		update the game state to the start of the next turn, and
		calculate reponses for each player.
		"""
		with self.action_list_lock:
			actions = self.actions[self.turn]
		results = {}
		refineries = [x.refinery for x in \
						  self.game_map.asteroids.itervalues() if x.refinery]
		bases = [x.base for x in self.game_map.planets.itervalues() if x.base]
		for obj in self.game_map.objects.itervalues():
			obj.events = []
		a = []
		a.extend(bases)
		a.extend(refineries)
		for obj in a:
			obj.events = []
		# execute orders
		with self.action_list_lock:
			for player in self.players.values():
				if player.auth in  actions.keys():
					p_actions = actions[player.auth]
					for action in p_actions:
						method = getattr(action['object'], action['method'])
						method(**action['params'])
				else:
					player.missed += 1
					if player.missed > 3:
						player.alive = False
						for obj in player.objects.values():
							obj._delete()

		# take timestep
		for object in self.game_map.objects.itervalues():
			object.step(1)
		#apply effects
		ownables = []
		ownables.extend(refineries)
		ownables.extend(bases)
		ownables.extend(self.game_map.ships.values())
		for obj in ownables:
			for event in obj.events:
				if event['type'] == 'damage':
					obj.health -= event['amount']
			if obj.health <= 0:
				# kill dead objects
				obj._delete()
			else:
				# compute radar returns for live ships
				nearships = self.game_map.radar(obj)
				for other in nearships:
					radar = {'type':'radar',
							 'obj_type': other.__class__.__name__,
							 'id': id(other),
							 'position':jitter_tuple(other.position, -75, 75)}
					if hasattr(other, 'health'):
						radar['health'] = other.health
					if hasattr(other, 'owner'):
						radar['owner'] = id(other.owner)
					if hasattr(other, 'refinery'):
						if other.refinery:
							radar['refinery'] = {
								'owner': id(other.refinery.owner),
								'id':id(other.refinery),
								'health': other.refinery.health}
						else: None
					if hasattr(other, 'base'):
						if other.base:
							radar['base'] ={
								'owner': id(other.base.owner),
								'id':id(other.base),
								'health': other.base.health}
						else: None
					obj.events.append(radar)			   
				obj.results[self.turn] = obj.events[:]

		# Create a massive list of results to return to the player
		with self.player_result_lock:
			self.player_results[self.turn] = {}
			for key, value in self.players.iteritems():
				self.player_results[self.turn][key] = \
					[object.to_dict() \
						 for object in value.objects.itervalues()]
			# kill players with no live units
				if len(value.ships) == 0 and len(value.bases) == 0:
					value.alive = False
				# update resources and scores
				value.update_resources()
				value.update_score()
					

		for object in self.game_map.objects.itervalues():
			object.results[self.turn + 1] = []
			if isinstance(object, Ship):
				for method in object.methods_used.iterkeys():
					object.methods_used[method] = False

		# subtract from busy and build counters
			if hasattr(object, 'base') and object.base != None:
				if object.base.built > 0:
					object.base.built -= 1
				if object.base.busy > 0:
					object.base.busy -= 1

			if hasattr(object, 'refinery') and object.refinery != None:
				if object.refinery.built > 0:
					object.refinery.built -= 1

		# advnace turn and reset timer
		with self.action_list_lock:
			self.actions.append({})
			self.completed_turns.append({})
			self.turn_condition.acquire()
			self.turn += 1
			self.turn_condition.notify()
			self.turn_condition.release()
		with self.lasers_shot_lock:
			self.lasers_shot.append([])
		self.last_turn_time = time.time()

	def _main(self):
		"""
		Game main thread. Polls for turns being ready.

		Started by _begin(). Calls _end when one player remains.
		Resolves a turn when timeout passes or all players have
		submitted moves.
		"""

		while self.active == True:
			alive_players = [x for x in self.players.itervalues() if x.alive]
			
			if len(alive_players) <= 1:
				self._end()
			else: 
				self.last_alive = alive_players
			if time.time() - self.start_time > 600:
				self._end()
			with self.action_list_lock:
				turns_submitted = len(self.completed_turns[self.turn])
			if turns_submitted == len(alive_players):
					self._resolve_turn()
			elif time.time() - self.last_turn_time > 2:
					self._resolve_turn()
			else:
				continue

	def wait_for_next(self, turn):
		"""
		Wait until the given turn, with a lock.
		@param turn: The turn to wait for.
		"""
		self.turn_condition.acquire()
		while self.turn < int(turn):
			self.turn_condition.wait()
		self.turn_condition.notify()
		self.turn_condition.release()

	def get_player_by_auth(self, auth):
		"""
		Get player object via their auth code.
		@param auth: auth string
		@rtype: Player object
		@return: Player object or None
		"""
		players = [x for x in self.players.values() if x.auth == auth]
		if len(players) > 0:
			return players[0]
		else:
			return None

	# API Calls

	def turn_number(self):
		"""
		Get turn number.

		@rtype: dictionary
		@return: Current turn as {'turn' : turn}.
		"""
		return {
			'turn': self.turn,
			'game_active': self.active
		}

	def game_status(self):
		"""
		Return basic game status.

		@rtype: dictionary
		@return: Dictionary with fields game_active, turn, and
				active_players, which contain the boolean status of the
				game, the upcoming turn, and the list of active players.
		"""
		active_players = []
		for player in self.players.itervalues():
			if player.alive:
				active_players.append(player.name)

		return {
			'game_active': self.active,
			'turn':self.turn,
			'active_players': active_players
		}

	def game_turn_get(self, auth, turn):
		"""
		Returns the player_results from the requested turn.
		"""
		if turn > 0 and turn < self.turn:
			player = self.get_player_by_auth(auth)
			if player == None:
				return {'success':False, 'message':'bad auth'}
			with self.player_result_lock:
				return player_results[turn - 1][id(player)]
		else:
			return {'success':False, 'message':'invalid turn number'}

	def game_avail_info(self, auth):
		"""
		Return game state including objects of player with given auth code.

		@type  auth: string
		@param auth: authCode of the player making the requests.
		"""
		alive_players = []
		for player in self.players.itervalues():
			if player.alive:
				alive_players.append(player.name)
		player = self.get_player_by_auth(auth)
		if player == None:
			return {'success':False, 'message':'bad auth'}

		return {
			'game_active': self.active,
			'turn':self.turn,
			'constants':Constants.to_dict(),
			'you': id(player),
			'resources': player.resources,
			'score':player.score,
			'alive_players': alive_players,
			'objects': [object.to_dict() for object in\
					player.objects.itervalues()],
		}

	def add_player(self, name, auth):
		from player import Player
		"""
		Adds a player to the current game, begin game if now full.

		@type  name: string
		@param name: Name of player

		@type  authToken: string
		@param authToken: player token
		"""
		if self.get_player_by_auth(auth):
			return {'success': False,
				'message': 'Already joined'}
		if auth not in self.allowed_auths:
			return {'success': False,
				'message': 'Not a valid auth code.'}
		if len(self.players.keys()) >= self.game_map.max_players:
			return {'success': False,
				'message': 'Game full'}

		new_player = Player(name, auth)
		self.players[id(new_player)] = new_player
		self._log(name + " joined the game.")

		if len(self.players.keys()) == self.game_map.max_players:
			self._begin()
		self.allowed_auths.remove(auth)
		return {'success': True,
			'message': 'Joined succesfully'}

	def game_visualizer(self, auth):
		"""
		Return all objects to the visualizer.

		@return: list of all objects
		"""
		if auth != self.viz_auth:
			return {'message':'not a valid auth code'}
		else:
			data = {'turn':self.turn, 
					'game_active': self.active,
					'objects':[], 
					'players':[p.to_dict() for p in self.players.values()], 
					'lasers':self.lasers_shot[self.turn - 1]}
			for o in self.game_map.objects.values():
				o_data = o.to_dict()
				if 'health' in o_data.keys():
					o_data['health'] = (o_data['health']*100.0/ \
										o_data['max_health'])
				if 'base' in o_data.keys() and o_data['base']:
					o_data['base']['health'] = \
						(o_data['base']['health']*100.0/o_data['base']['max_health'])
				if 'refinery' in o_data.keys() and o_data['refinery']:
					o_data['refinery']['health']= (o_data['refinery']['health']*100.0/ \
												   o_data['refinery']['max_health'])
				data['objects'].append(o_data)
			return data
			
class TestGame(unittest.TestCase):
	def setUp(self):
		from game_map import Map
		self.game_map = Map(2)
		self.game = Game(self.game_map,"test_log")

	def tearDown(self):
		self.game.active = False
		# thread should eventually kill itself, if it is running
		del self.game_map
		del self.game

if __name__ == '__main__':
	unittest.main()
