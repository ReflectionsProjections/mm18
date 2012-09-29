#! /usr/bin/env python

import constants

## @file units.py

## This class is for the attack units.
#  Each unit is just one thing.
class Unit:

	## Creates a new offensive Unit with health, a level and a specialisation.
	#  @param level The level the unit is.  Cannot be changed once created.
	#  @param spec The specialisation the unit has
	#  @param player The player the unit belongs to
	def __init__(self, level, spec, player):
			self.level = level
			self.specialisation = spec
			self.health = constants.BASE_UNIT_HEALTH*constants.UNIT_UPGRADE_MULTIPLIER[self.level]
			self.owner = player.name
	
	## Static method for the player to purchase the units.
	#  @param level The level the unit is.  Cannot be changed once created.
	#  @param spec The specialisation the unit has
	#  @param player The player the unit belongs to
	@staticmethod
	def purchaseUnit(level, spec, player):
		if player.allowedUpgrade >= level and player.purchaseCheck(constants.UNIT_BASE_COST*constants.UNIT_UPGRADE_COST[level]) and spec >= -1 and spec <=1:
			player.purchase(constants.UNIT_BASE_COST*constants.UNIT_UPGRADE_COST[level])
			player.sentUnits += 1
			player.increaseUpgrade()
			return Unit(level, spec, player)
		else:
			return None
			
	## Take damage from a tower.
	#  @param amount The amount of damage
	#  @param specialisation The tower specialisation
	def damage(self, amount, specialisation):
		multiplier = constants.specialisation_mulitplier(specialisation, self.specialisation)
		self.health -= amount*multiplier

	## Damage this unit does when it reaches the base.
	def finalDamage(self):
		return (constants.BASE_UNIT_DAMAGE
			*constants.UNIT_UPGRADE_MULTIPLIER[self.level]
			*(self.health / constants.BASE_UNIT_HEALTH))