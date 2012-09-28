#! /usr/bin/env python

import mm18.game.constants
from mm18.game.board import Board
from mm18.game.player import Player
import time

class Engine():

	def __init__(self):

		#generate players and boards
		self.players = {}
		self.numDead = 0
		self.curTick = 0
		self.running = True

		#this is an id that will be used for giving towers
		#a unique identifier
		self.currID = 0

	# Game controls

	def add_player(self, id):
		board = Board.jsonLoad('board1.json')
		player = Player(id, board)
		self.players[id] = player
		return player
	
	def run(self):
		if self.players:
			while self.running:
				advance()
	

	def advance(self):
		self.oldtime=time.time()
		self.curTick += 1;
		#if self.curTick >= 300000000: #game timeout
		#	endGame()
		#if self.curTick >= 1000000:
		#	self.curTick = self.curTick%1000000	
		if self.curTick%constants.SUPPLY_TIME == 0:
			supply() 
		moveUnits() 
		countDead() 
		towerResponses()
		if self.numDead == 3 :
			endGame()
		self.pasttime = time.time()-oldtime	
		if constants.TICK_TIME-pasttime > 0 :
			time.sleep(TICK_TIME-pasttime)

	def supply(self):
		maxTier = max(self.players.iterkeys(), key=allowedUpgrade)
		resources = BASE_RESOURCES + UPGRADE_INCREASE * maxTier
		for player in players.iteritems():
			player.addResources(resources)

	def moveUnits(self):
		for player in players.iteritems():
			if not player.isDead():
				player.board.moveUnits()

	def countDead(self):
		count = sum(1 for player in players.iteritems() if player.isDead())
		if count > self.numDead:
			self.numDead = count
		return count

	def towerResponses(self):
		for player in players.iteritems():
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
		return self.get_player(owner_id).purchaseTower()

	""" This should return the upgraded tower """
	def tower_upgrade(self, tower_id, owner_id):
		pass

	""" This should return the player object relating to owner_id """
	def tower_sell(self, tower_id, owner_id):
		pass

	""" This should return the tower that's been specialized """
	def tower_specialize(self, tower_id, owner_id, spec):
		pass

	""" This should return the tower that's been specified """
	def tower_get(self, tower_id, player_id):
		pass

	# Unit Class Controls

	""" This should return the object of the unit """
	def unit_create(self, owner_id, level, spec, target_id, path):
		pass
