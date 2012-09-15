#! /usr/bin/env python

import constants

"""
This class is for the attack units.
Each unit is just one thing.
"""

class Unit:

	"""
	Creates a new offensive Unit with health, a level and a specialisation.
	
	level -- the level the unit is.  Cannot be changed once created.
	spec -- the specialisation the unit has
	player -- the player the unit belongs to
	"""
	def __init__(self, level, spec, player, pathID):
			self.level = level
			self.specialisation = spec
			self.health = constants.BASE_UNIT_HEALTH*constants.UNIT_UPGRADE_MULTIPLIER[self.level]
			self.owner = player.name
			self.pathID = pathID
	
	"""
	Static method for the player to purchase the units

	level -- the level the unit is.  Cannot be changed once created.
	spec -- the specialisation the unit has
	player -- the player the unit belongs to
	"""
	@staticmethod
	def purchaseUnit(level, spec, player, pathID):
		if player.allowedUpgrade >= level and player.purchaseCheck(constants.UNIT_BASE_COST*constants.UNIT_UPGRADE_COST[level]) and spec >= -1 and spec <=1:
			player.purchase(constants.UNIT_BASE_COST*constants.UNIT_UPGRADE_COST[level])
			player.sentUnits += 1
			player.increaseUpgrade()
			return Unit(level, spec, player, pathID)
		else:
			return None
