#! /usr/bin/env python

import json
import time
import threading

import constants
from board import Board
from player import Player
from units import Unit

class Engine():

	@staticmethod
	def spawn_game(players, game_log):
		log = None
		if game_log != None and game_log != "":
			log = open(game_log, "w+")
		engine = Engine(log)
		for player in players:
			engine.add_player(player)
		engine.log_start()

		thread = threading.Thread(target=engine.run)
		thread.start()
		return engine

	def __init__(self, log_file=None):
		self.log_file = log_file

		#generate players and boards
		self.players = {}
		self.currTick = 0
		self.running = True

		#this is an id that will be used for giving towers
		#a unique identifier
		self.currID = 0

	def log_action(self, action_type, **kwargs):
		if self.log_file:
			entry = dict(kwargs)
			entry['action'] = action_type
			action = json.dumps(entry)
			self.log_file.write(action + '\n')

	def log_start(self):
		self.log_action('start', tick=self.currTick)

	# Game controls

	def add_player(self, id):
		board = Board.jsonLoad('board2.json')
		# Force the id to be a string
		id = str(id)
		player = Player(id, board)
		self.players[id] = player

		self.log_action('add_player', id=id)

		return player

	def run(self):
		turns=0
		while self.running:
			startTime = time.time()
			self.advance()
			self.check_running()
			timePassed = time.time() - startTime
			if timePassed < constants.TICK_TIME:
				time.sleep(constants.TICK_TIME - timePassed)
			turns=turns+1
			if turns > constants.MAX_RUNTIME:
				self.endGame()

		print "Game complete"

	def advance(self):
		self.currTick = self.currTick + 1
		if self.currTick % constants.SUPPLY_TIME == 0:
			self.supply()

		# Create a dict that will contain a summary of all events
		# that occurr in the tick on each Player's Board
		summary = {}
		for player in self.players.itervalues():
			if not player.isDead():
				summary[player.name] = player.advance()

		self.log_action('advance', tick=self.currTick)

		return summary

	def check_running(self):
		alive = sum(1 for player in self.players.itervalues() \
				if not player.isDead())
		if alive <= 1:
			self.endGame()
		if self.currTick > constants.MAX_RUNTIME:
			self.endGame()

	def supply(self):
		maxTier = max(player.allowedUpgrade for player in self.players.itervalues())
		resources = constants.BASE_RESOURCES + constants.UPGRADE_INCREASE * maxTier
		for player in self.players.itervalues():
			player.addResources(resources)

	def endGame(self):
		self.running=False
		highScore=0
		for player in self.players.itervalues():
			if (player.resources+1)*player.health <= highScore:
				player.damage(constants.BASE_HEALTH)
			else:
				highScore=(player.resources+1)*player.health

	def generateID(self):
		retID = self.currID
		self.currID = self.currID + 1
		return retID
	
	# Player controls

	""" This should return a list of all player IDs """
	def get_player_ids(self):
		return self.players.keys()

	""" This should return a player object """
	def get_player(self, player_id):
		return self.players.get(str(player_id))

	# Board Class Controls

	""" This should return the board of player_id """
	def board_get(self, player_id):
		return self.get_player(player_id).board

	# Tower Class Controls

	""" This should return the tower object that's created """
	def tower_create(self, owner_id, coords):
		tower = self.get_player(owner_id).purchaseTower(coords, self.generateID())

		self.log_action('tower_create', owner_id=owner_id, coords=list(coords))

		return tower

	""" This should return the tower that's been specified"""
	def tower_get(self, tower_id, owner_id=None):
		# If an owner id is given, only search that Player's Towers
		if owner_id:
			players = [self.get_player(owner_id)]
		else:
			players = self.players.values()

		for player in players:
			board = player.boardIs()
			towers = board.getTowers()

			for tower in towers.itervalues():
				if tower.getID() == tower_id:
					return tower

		return None

	""" This should return the player object relating to owner_id """
	def tower_sell(self, tower_id, owner_id):
		retPlayer = self.get_player(owner_id)
		if retPlayer == None:
			return retPlayer

		tower = self.tower_get(tower_id, owner_id)
		if tower == None:
			return retPlayer

		retPlayer.sellTower(retPlayer.board.getTowerPosition(tower_id))

		self.log_action('tower_sell', tower_id=tower_id, owner_id=owner_id)

		return retPlayer

	""" This should return the tower that's been specialized """
	def tower_specialize(self, tower_id, owner_id, spec):
		retTower = self.tower_get(tower_id, owner_id)
		if(retTower == None):
			return None

		player = self.get_player(owner_id)

		if(player == None):
			return None

		retTower.specialise(spec)

		self.log_action('tower_specialize', tower_id=tower_id,
			owner_id=owner_id, spec=spec)

		return retTower

	""" This should return the tower that's been specified """
	def tower_upgrade(self, tower_id, owner_id):
		retTower = self.tower_get(tower_id, owner_id)
		board = self.board_get(owner_id)
		towers = board.getTowers()
		coords = None

		for elem in towers:
			if towers[elem].ID == tower_id:
				coords = elem

		if(retTower == None):
			return None

		player = self.get_player(owner_id)

		if(player == None):
			return None

		retTower.upgradeTower(player)
		player.refreshTower(coords, retTower)

		self.log_action('tower_upgrade', tower_id=tower_id, owner_id=owner_id)

		return retTower

	# Unit Class Controls

	""" This should return the object of the unit """
	def unit_create(self, owner_id, level, spec, target_id, direction):
		player = self.get_player(owner_id)

		if(player == None):
			return None

		board = self.board_get(target_id)

		if(board == None):
			return None

		retUnit = Unit.purchaseUnit(level, spec, player)

		self.log_action('unit_create', owner_id=owner_id, level=level,
			spec=spec, target_id=target_id, direction=direction)

		if retUnit != None:
			if(board.queueUnit(retUnit, direction)):
				return retUnit

		return None
