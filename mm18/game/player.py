#! /usr/bin/env python

import constants

"""For player stuff"""

class Player:

	"""
	Creates a player with a base number of resources

	name -- player name
	"""

	def __init__(self, name):
		self.resources = constants.BASE_RESOURCES
		self.name = name
		self.allowedUpgrade = 0


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

