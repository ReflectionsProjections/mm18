#! /usr/bin/env python

import constants

"""
This class is for the attack units.
Each unit is just one thing.
"""

class Units:

	"""
	Creates a new offensive Unit with health, a level and a specialisation.
	
	level -- the level the unit is.  Cannot be changed once created.
	spec -- the specialisation the unit has
	player -- the player the unit belongs to
	"""

	def __init__(self, level, spec, player):
		if player.allowedUpgrade <= level and player.purchase(constants.UNIT_BASE_COST):
			self.level = level
			self.specialisation = spec
			self.health = constants.BASE_UNIT_HEALTH*constants.UPGRADE_MULTIPLIER[self.level]
			self.owner = player.name
			player.sentUnits += 1
			player.increaseUpgrade()
