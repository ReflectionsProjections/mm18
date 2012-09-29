#! /usr/bin/env python

import time

import constants
from board import Board
from player import Player
from units import Unit

class Engine():

	def __init__(self):

		#generate players and boards
		self.players = {}
		self.currTick = 0
		self.running = True

		#this is an id that will be used for giving towers
		#a unique identifier
		self.currID = 0

	def log_action(self, action_type, **kwargs):
		pass

	# Game controls

	def add_player(self, id):
		board = Board.jsonLoad('board1.json')
		player = Player(id, board)
		self.players[id] = player

		self.log_action('add_player', id=id)

		return player

	def run(self):
		while self.running:
			startTime = time.time()
			self.advance()
			self.check_running()
			timePassed = time.time() - startTime
			if timePassed < constants.TICK_TIME:
				time.sleep(constants.TICK_TIME - timePassed)

	def advance(self):
		self.currTick = self.currTick + 1
		if self.currTick % constants.SUPPLY_TIME == 0:
			self.supply()
		self.moveUnits()
		self.towerResponses()

		self.log_action('advance', tick=self.currTick)

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

	def moveUnits(self):
		for player in self.players.itervalues():
			if not player.isDead():
				player.board.moveUnits()

	def towerResponses(self):
		for player in self.players.itervalues():
			if not player.isDead():
				player.board.fireTowers()

	def endGame(self):
		self.running = False

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
		return self.players.get(player_id)

	# Board Class Controls

	""" This should return the board of player_id """
	def board_get(self, player_id):
		return self.get_player(player_id).board

	# Tower Class Controls

	""" This should return the tower object that's created """
	def tower_create(self, owner_id, coords, level=1, spec=0):
		tower = self.get_player(owner_id).purchaseTower(coords, self.generateID())

		self.log_action('tower_create', owner_id=owner_id, coords=list(coords))

		return tower

	""" This should return the tower that's been specified"""
	def tower_get(self, tower_id, owner_id):
		player = self.get_player(owner_id)
		if(player == None):
			return None

		board = player.boardIs()
		towers = board.getTowers()

		retTower = None

		for elem in towers:
			if elem.getID == tower_id:
				retTower = elem
				break

		
		return retTower

	""" This should return the player object relating to owner_id """
	def tower_sell(self, tower_id, owner_id):
		retPlayer = get_player(owner_id)
		if retPlayer == None:
			return retPlayer

		tower = get_tower(tower_id, owner_id)
		if tower == None:
			return retPlayer

		player.sellTower(tower.position)

		self.log_action('tower_sell', tower_id=tower_id, owner_id=owner_id)

		return retPlayer		

	""" This should return the tower that's been specialized """
	def tower_specialize(self, tower_id, owner_id, spec):
		retTower = tower_get(tower_id, owner_id)
		if(retTower == None):
			return None

		player = get_player(owner_id)

		if(player == None):
			return None

		retTower.specialise(spec, player)

		self.log_action('tower_specialize', tower_id=tower_id,
			owner_id=owner_id, spec=spec)

		return tower		

	""" This should return the tower that's been specified """
	def tower_upgrade(self, tower_id, player_id):
		retTower = tower_get(tower_id, owner_id)
		if(retTower == None):
			return None

		player = get_player(owner_id)

		if(player == None):
			return None

		retTower.specialise(spec, player)

		self.log_action('tower_upgrade', tower_id=tower_id, player_id=player_id)

		return tower

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
		board.queueUnit(retUnit, direction)

		self.log_action('unit_create', owner_id=owner_id, level=level,
			spec=spec, target_id=target_id, direction=direction)

		return retUnit
