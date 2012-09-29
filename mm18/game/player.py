#! /usr/bin/env python

import constants
from tower import Tower
from types import *

## @file player.py
#  @brief A Python program for player stuff

## A class to hold all player-related functions.
#  Any function related to the player should be in this class.
class Player:

# INSTANTIATION
# =============================================================================

	## Create a player with a base number of resources.
	#  Each player cannot upgrade their towers/units past their allowed upgrade.
	#  @param name The player's name
	#  @param board The board the player should be added to
	def __init__(self, name, board):
		self.name = name
		self.board = board

		self.resources = constants.BASE_RESOURCES
		self.health = constants.BASE_HEALTH

		self.allowedUpgrade = 1
		self.sentUnits = 0


# FUNCTIONS
# =============================================================================

	## Increases the allowed upgrade level of the player.
	def increaseUpgrade(self):
		if self.sentUnits >= constants.UPGRADE_INCREASE*(self.allowedUpgrade+1):
			self.allowedUpgrade += 1
			return True
		else:
			return False
			
	## Purchase method to make purchases.
	#  @param cost The cost of the purchase
	def purchase(self,cost):
		self.resources -= cost

	## Method checks whether a user has enough resources to go through with a purchase.
	#  @param cost The cost of the purchase
	#  @return true if the player has sufficient resources for the purchase and false otherwise
	def purchaseCheck(self, cost):
		assert type(cost) is IntType
		if self.resources >= cost:
			return True
		else:
			return False

	## Damage method to take damage.
	#  @param damage Amount of damage a player takes
	def damage(self, damage):
		self.health -= damage

	## Static method for the player to purchase the tower that has been created.
	#  @param player The player who is purchasing the tower
	def purchaseTower(self, coords=None, ID=0):
		if self.purchaseCheck(constants.TOWER_BASE_COST):
			self.purchase(constants.TOWER_BASE_COST)
			t = Tower(self, ID)
			if coords:
				self.board.addItem(t, coords)
			return t
		else:
			return None

	## Sells the tower
	def sellTower(self, position):
		"""
		Sells the tower
		"""
		tower = player.board.getItem(position)
		if tower is not None:
			self.resources += tower.cost * TOWER_SELL_SCALAR
			self.board.removeItem(position)

# GETTERS / SETTERS
# =============================================================================

	## Method checks whether a user is dead or not.
	#  @return true if dead or false if alive
	def isDead(self):
		return self.health <= 0

	## Method return player health.
	#  @return Remaining health of player
	def healthIs(self):
		return self.health

	## Method returns player resources
	#  @return Player resources
	def resourcesIs(self):
		return self.resources

	## Method returns allowed upgrade level of player
	#  @return Allowed upgrade level
	def allowedUpgradeIs(self):
		return self.allowedUpgrade

	## Method returns board of player
	# @return The board of the player
	def boardIs(self):
		return self.board

	## Method to add resources to a player
	#  @param ammount Number of resources to add
	def addResources(self, ammount):
		self.resources += ammount
