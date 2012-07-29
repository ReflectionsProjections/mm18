#! /usr/bin/env python

import constants

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
		self.allowedUpgrade = 0
		self.sentUnits = 0

	"""
	Increases the allowed upgrade level of the player
	"""

	def increaseUpgrade(self):
		if self.sentUnits >= constants.UPGRADE_INCREASE*(self.allowedUpgrade+1)
			allowedUpgrade += 1
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
		if self.resources >= cost:
			return True
		else:
			return False

