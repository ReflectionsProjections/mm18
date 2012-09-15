#! /usr/bin/env python

import constants
from types import *

"""For player stuff"""

class Player:

	"""
	Creates a player with a base number of resources.
	Each player cannot upgrade their towers/units past their allowed upgrade.

	name -- player name
	"""

	def __init__(self, name):
		self.resources = constants.BASE_RESOURCES
		self.name = name
		self.allowedUpgrade = 1
		self.sentUnits = 0
		self.health = constants.BASE_HEALTH

	"""
	Increases the allowed upgrade level of the player
	"""

	def increaseUpgrade(self):
		if self.sentUnits >= constants.UPGRADE_INCREASE*(self.allowedUpgrade+1):
			self.allowedUpgrade += 1
			return True
		else:
			return False


	"""
	Purchase method to make purchases

	cost -- The cost of the purchase
	"""

	def purchase(self,cost):
		self.resources -= cost

	"""
	Method checks whether a user has enough resources to go through with a purchase.

	cost -- the cost of the purchase
	"""

	def purchaseCheck(self, cost):
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
		if self.health > 0:
			return False
		else:
			return True


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

