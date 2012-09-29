#! /usr/bin/env python

import constants

## @file tower.py

## This is the tower class.
#  Towers get created here.
#  All towers need:
#	-A position
#	-A specialisation (or lack)
#	-Tower upgrade level
class Tower:

	## Creates a new Tower.
	#  All towers start with 0 upgrades, no specialisation and no position.
	#  @param player The player who owns the tower
	def __init__ (self, player, ID):
		self.upgrade = 1
		self.specialisation = 0
		self.cost = constants.TOWER_BASE_COST
		self.owner = player
		self.ID = ID

	## Upgrades the tower.
	#  @param player The player upgrading the tower
	def upgradeTower(self, player):
		if self.upgrade == constants.MAX_UPGRADE:
			return False #fully upgraded
		elif player.allowedUpgrade > self.upgrade and player.purchaseCheck(constants.TOWER_UPGRADE_COST[self.upgrade + 1]):
			player.purchase(constants.TOWER_UPGRADE_COST[self.upgrade + 1])
			self.cost = constants.TOWER_UPGRADE_COST[self.upgrade + 1]
			self.upgrade += 1
			return True #level increase, resources decrease
		else:
			return False #Sommat fucked up or not enough resources

	## Specializes the tower.provided the towers have not been upgraded and specialisation input is valid.
	#  Currently using 0 for no specialisation and 1, -1 for the different ones.
	#  @param spec Either 1, 0 or -1.  Indicates a specialisation.
	#  @param player The player specializing the tower
	def specialise(self, spec):
		if self.upgrade == 1 and spec >= -1 and spec <= 1 and \
				spec != self.specialisation and \
				self.owner.purchaseCheck(constants.TOWER_SPECIALIZE_COST[self.upgrade]):
			self.owner.purchase(constants.TOWER_SPECIALIZE_COST[self.upgrade])
			self.cost = constants.TOWER_SPECIALIZE_COST[self.upgrade]
			self.specialisation += spec
			return True #special changes, resources decrease
		else:
			return False #Sommat fucked up or not enough resources

	## Damage the attacked unit.
	def fire(self, unit):
		unit.damage(constants.TOWER_UPGRADE_MULTIPLIER[self.upgrade]
                    * constants.BASE_TOWER_DAMAGE,
					self.specialisation)

	def getID(self):
		return ID
