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

	"""
	Damage method to take damage
	
	damage - amount of damage a player takes

	"""

	def damage(self, damage):
		self.health -= damage

	"""
	Method checks whether a user is dead or not
	"""

	def isDead(self):
		return self.health <= 0


	"""
	Method returns player health
	"""

	def healthIs(self):
		return self.health
		
	"""
	Method returns player resources
	"""
	
	def resourcesIs(self):
		return self.resources
		
	"""
	Method returns allowed upgrade level of player
	"""
	
	def allowedUpgradeIs(self):
		return self.allowedUpgrade
		
	"""
	Method to add resources to a player
	"""
	
	def addResources(self, ammount):
		self.resources += ammount
