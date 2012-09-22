#! /usr/bin/env python

import mm18.game.constants
from mm18.game.board import Board
from mm18.game.player import Player
import time

class Engine():

	def __init__(self):

		#generate players and boards
		self.players = []
		for i in range(0-4)
			self.players.append(Player(i))
		self.boards = []
		for i in range(0-4)
			self.boards.append(Board([(0,1),(1,1)],[(0,2),(1,2),(1,3),(0,4)]))
		self.maxtier = 0
		self.numDead = 0
		self.curTick = 0
		self.oldtime
		self.pasttime

	# Game controls

	def advance(self):
		self.oldtime=time.time()
		self.curTick += 1;
		if self.curTick >= 300000000: #game timeout
			endGame()
		#if self.curTick >= 1000000:
		#	self.curTick = self.curTick%1000000	
		if self.curTick%constants.SUPPLY_TIME == 0:
			supply() 
		moveUnits() 
		countDead() 
		towerResponces()
		if self.numDead == 3 :
			endGame()
		self.pasttime = time.time()-oldtime	
		if constants.TICK_TIME-pasttime > 0 
			time.sleep(TICK_TIME-pasttime)
		
			

	def supply(self):
		for i in self.get_player_ids():
				if self.get_player(i).self.get_player(i).allowedUpgradeIs() > self.maxtier :
					self.maxtier = self.get_player(i).allowedUpgradeIs()

		for i in self.get_player_ids():
				self.get_player(i).addResource(BASE_RESOURCES + UPGRADE_INCREASE*self.maxtier)
	
	def moveUnits(self):
		# moveunits on all valid boards
		#for all players : player.board.moveunits
		pass
	
	def countDead(self):
		count = 0
		for i in self.get_player_ids():
			if self.get_player(i).isDead(): count += 1
		if count > self.numDead: self.numDead = count
	
	def towerResponces(self):
		# all towers attack
		#for all players : player.board.useTowers
		pass

	def endGame(self):
		# endGamecondition
		pass
	
	# Player controls

	def get_player_ids(self):
		pass

	def get_player(self, player_id):
		pass

	# Board Class Controls

	def get_board(self, player_id):
		pass

	# Tower Class Controls

	def tower_create(self, owner_id, coords, level, spec):
		pass

	def tower_upgrade(self, tower_id, owner_id):
		pass

	def tower_sell(self, tower_id, owner_id):
		pass

	def tower_specialize(self, tower_id, owner_id, spec):
		pass

	# Unit Class Controls

	def unit_create(self, owner_id, level, spec, target_id, path):
		pass
