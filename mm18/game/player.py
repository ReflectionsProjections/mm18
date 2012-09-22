#! /usr/bin/env python

import constants
from types import *

## \file player.py
## \brief A Python program for player stuff


# Player class
class Player:
	""" \brief A class to hold all player-related functions
	
	Any function related to the player should be in this class.
	"""

	def __init__(self, name):
		"""Create a player with a base number of resources.
		
		Each player cannot upgrade their towers/units past their allowed upgrade.
		
		\param name The player's name
		"""
		self.resources = constants.BASE_RESOURCES
		self.name = name
		self.allowedUpgrade = 1
		self.sentUnits = 0
		self.health = constants.BASE_HEALTH

	def increaseUpgrade(self):
		"""Increases the allowed upgrade level of the player
		"""
		if self.sentUnits >= constants.UPGRADE_INCREASE*(self.allowedUpgrade+1):
			self.allowedUpgrade += 1
			return True
		else:
			return False

	def purchase(self,cost):
		"""Purchase method to make purchases
		
		\param cost The cost of the purchase
		"""
		self.resources -= cost

	def purchaseCheck(self, cost):
		"""Method checks whether a user has enough resources to go through with a purchase.
		
		\param cost The cost of the purchase
		\return true if the player has sufficient resources for the purchase and false otherwise
		"""
		assert type(cost) is IntType
		if self.resources >= cost:
			return True
		else:
			return False

	def damage(self, damage):
		"""Damage method to take damage
		
		\param damage Amount of damage a player takes
		"""
		self.health -= damage

	def isDead(self):
		"""Method checks whether a user is dead or not
		
		\return true if dead or false if alive
		"""
		return self.health <= 0

	def healthIs(self):
		"""Method returns player health
		
		\return Remaining health of player
		"""
		return self.health
		
	def resourcesIs(self):
		"""Method returns player resources
		
		\return Player resources
		"""
		return self.resources
		
	def allowedUpgradeIs(self):
		"""Method returns allowed upgrade level of player
		
		\return Allowed upgrade level
		"""
		return self.allowedUpgrade
		
	def addResources(self, ammount):
		"""Method to add resources to a player
		
		\param ammount Number of resources to add
		"""
		self.resources += ammount
