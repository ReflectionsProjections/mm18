#! /usr/bin/env python

import constants

"""
This is the tower class
Towers get created here.
I'm thinking have this as a superclass and make the specialised classes from this?
Or not - it may just be easier to put it all in here because towers don't need a lot
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
	def __init__ (self):
		self.upgrade = 0 
		self.specialisation = 0

	"""
	Static method for the player to purchase the tower that has been created

	player -- the player who is purchasing the tower
	"""
	@staticmethod
	def purchaseTower(player):
		if player.purchaseCheck(constants.TOWER_BASE_COST):
			player.purchase(constants.TOWER_BASE_COST)
			return Tower()
		else:
			return None

	"""
	Upgrades the tower.
	
	player -- The player upgrading the tower
	"""
	def upgradeTower(self, player):
		if self.upgrade == constants.MAX_UPGRADE:
			print "Fully upgraded"
		elif player.allowedUpgrade > self.upgrade and player.purchaseCheck(constants.UPGRADE_COST[self.upgrade + 1]):
			player.purchase(constants.UPGRADE_COST[self.upgrade + 1])
			self.upgrade += 1
			print "Tower level is now:", self.upgrade, "\nPlayer resources are now:", player.resources
		else:
			print "Sommat fucked up or not enough resources"

	"""
	Specialises the towers provided the towers have not been upgraded and specialisation input is valid.
	Currently using 0 for no specialisation and 1, -1 for the different ones.

	spec -- either 1, 0 or -1.  Indicates a specialisation.
	"""
	def specialise(self,spec):
		if self.upgrade == 0 & spec >= -1 & spec <= 1:
			self.specialisation = spec
			print "New specialisation is:", self.specialisation
		else:
			print "Either spec is not valid or object is already upgraded"

