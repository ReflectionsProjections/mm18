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

		#this is an id that will be used for giving towers
		#a unique identifier
		self.currID = 0
		


	def setBoardname():
		 self.mapName="board1.json"

	def makeBoards(self):
		newBoard= Board(Board.jsonLoad(self.mapName))
		self.boards.append(newBoard)
		return self.boards.newBoard

	# Game controls

	def addPlayer(self, name):
		self.boards.append(makeboard())
		self.players.append(Player(name, boards[len(boards) - 1]))
	
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
		towerResponces()
		if self.numDead == 3 :
			endGame()
		self.pasttime = time.time()-oldtime	
		if constants.TICK_TIME-pasttime > 0 :
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
		for i in range(0-len(players)):
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

	def generateID(self):
		retID = self.currID
		self.currID = self.currID + 1
		return retID
	
	# Player controls

	""" This should return a list of all player IDs """
	def get_player_ids(self):
		ids = []

		for elem in self.players:
			ids.append(elem.nameIs())

		return ids

	""" This should return a player object """
	def get_player(self, player_id):
		retPlayer = None

		for elem in self.players:
			if(elem.nameIs() == player_id):
				retPlayer = elem.nameIs()
				break
		
		return retPlayer

	# Board Class Controls

	""" This should return the board of player_id """
	def board_get(self, player_id):

		retBoard = None

		for elem in self.players:
			if(elem.nameIs() == player_id):
				retBoard = elem.boardIs()
				break

		return retBoard

	# Tower Class Controls

	""" This should return the tower object that's created """
	def tower_create(self, owner_id, coords, level, spec):
		towerRet = None
		for elem in self.players:
			if(elem.nameIs() == owner_id):
				towerRet = elem.purchaseTower()

		return towerRet

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
