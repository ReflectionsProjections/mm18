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


	"""
	Checks whether the player has enough resources to make a purchase
	If they can it also deducts the purchase amount.

	cost -- The cost of the upgrade
	"""

	def purchase(self, cost):
		if self.resources >= cost:
			self.resources -= cost
			return True
		else:
			return False

