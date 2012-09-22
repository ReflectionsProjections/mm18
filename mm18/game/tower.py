#! /usr/bin/env python

import constants

"""
This is the tower class
Towers get created here.
All towers need:
	-A position
	-A specialisation (or lack)
	-Tower upgrade level
"""

class Tower:

	"""
	Creates a new Tower.
	All towers start with 0 upgrades, no specialisation and no position.
	"""
	def __init__ (self, player):
		self.upgrade = 1
		self.specialisation = 0
		self.cost = constants.TOWER_BASE_COST
		self.owner = player

	"""
	Static method for the player to purchase the tower that has been created

	player -- the player who is purchasing the tower
	"""
	@staticmethod
	def purchaseTower(player):
		if player.purchaseCheck(constants.TOWER_BASE_COST):
			player.purchase(constants.TOWER_BASE_COST)
			return Tower(player)
		else:
			return None

	"""
	Upgrades the tower.
	
	player -- The player upgrading the tower
	"""
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

	"""
	Specialises the towers provided the towers have not been upgraded and specialisation input is valid.
	Currently using 0 for no specialisation and 1, -1 for the different ones.

	spec -- either 1, 0 or -1.  Indicates a specialisation.
	"""
	def specialise(self,spec):
		if self.upgrade == 1 and spec >= -1 and spec <= 1:
			self.specialisation = spec
			return True #new spec
		else:
			return False #either already upgraded or not valid

	"""
	Sells the tower
	"""
	@staticmethod
	def sellTower(player, tower):
		if tower.owner == player:
			player.resources += tower.cost*TOWER_SELL_SCALAR
			tower = null
		else:
			None

	"""
	Damage the attacked unit
	"""
	def fire(self, unit):
		unit.damage(constants.TOWER_UPGRADE_MULTIPLIER[self.upgrade]*constants.BASE_TOWER_DAMAGE,
		            self.specialisation)
