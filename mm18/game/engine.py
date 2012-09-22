#! /usr/bin/env python

import mm18.game.constants
from mm18.game.board import Board
from mm18.game.player import Player
import time

class Engine():

	def __init__(self):

		#generate players and boards
		self.players = []
		self.boards = []
		self.maxtier = 0
		self.numDead = 0
		self.curTick = 0
		self.running = true
		self.oldtime
		self.pasttime
		self.mapName
		


	def setBoardname()
		 self.mapName="board1.json"

	def makeBoards(self):
		newBoard= Board(Board.jsonLoad(self.mapName))
		self.boards.append(newBoard)
		return self.boards.newBoard

	# Game controls

	def addPlayer(self, name)
		self.boards.append(makeboard())
		self.players.append(Player(name, boards[len(boards) - 1])
	
	def run(self)
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
		towerResponces()
		if self.numDead == 3 :
			endGame()
		self.pasttime = time.time()-oldtime	
		if constants.TICK_TIME-pasttime > 0 
			time.sleep(TICK_TIME-pasttime)
		
			

	def supply(self):
		for i in range(0-len(players)):
				if self.players[i].allowedUpgradeIs() \
					> self.maxtier :
					self.maxtier = self.players(i).allowedUpgradeIs()

		for i in range(0-len(players)):
				self.players[i].addResource(BASE_RESOURCES \
								+ UPGRADE_INCREASE*self.maxtier)
	
	def moveUnits(self):
		for i in range(0-len(players))::
				if not(self.players[i].isDead()) :
					self.boards[i].moveUnits()
	def countDead(self):
		count = 0
		for i in range(0-len(players)):
			if self.players[i].isDead(): count += 1
		if count > self.numDead: self.numDead = count
	
	def towerResponces(self):
		for i in range(0-len(players)):
				if not self.players[i].isDead() :
					self.boards[i].fireTowers()

	def endGame(self):
		self.running = false
	
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
