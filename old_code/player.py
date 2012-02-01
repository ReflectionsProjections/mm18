#! /usr/bin/env python

import unittest

import Constants


class Player(object):
	def __init__(self, name, auth):
		"""
		Create a new player representation.
		
		@param name: The name of the new player
		@param auth_token: Authorization code for the payer (unique)
		"""
		from ship import Ship
		from asteroid import Refinery
		from planet import Base

		self.name = name
		self.auth = auth
		self.alive = True
		self.missed = 0
		self.resources = Constants.start_resources
		self.objects = {}
		self.ships = {}
		self.bases = {}
		self.refineries = {}
		self.score = 0
		self.dicts = [self.objects,
					  self.ships,
					  self.bases,
					  self.refineries]

	def add_object(self, obj):
		from ship import Ship
		from planet import Base
		from asteroid import Refinery
		"""
		Add an object to the player's directory.

		@param obj: The object to add.
		"""
		objID = id(obj)
		if objID not in self.objects.keys():
			self.objects[objID] = obj
		if isinstance(obj, Ship):
			self.ships[objID] = obj
		elif isinstance(obj, Base):
			self.bases[objID] = obj
		elif isinstance(obj, Refinery):
			self.refineries[objID] = obj
		return objID

	def update_score(self):
		"""
		Update the player score every turn.
		"""
		if self.alive:
			# Stockpiling resources alone shouldn't win
			score = self.resources * Constants.resource_multiplier
			for s in self.ships.values():
				salvaged = (float(s.health)/Constants.ship_health)*\
					Constants.salvage_multiplier
				score += salvaged
			for b in self.bases:
				score += Constants.base_price
			for r in self.refineries:
				score += Constants.refinery_price
			self.score = score

	def update_resources(self):
		"""
		Update the player's resources every turn.
		"""
		for refinery in self.refineries.values():
			if refinery.built == 0:
				self.resources += Constants.resource_pull
				refinery.asteroid.pull_resources
		for base in self.bases.values():
			if base.built == 0:
				self.resources += Constants.base_resource_pull
		if self.resources < 0:
			self.resources = 0


	def to_dict(self):
		"""
		Return the current state in JSON serializable representation.

		@type: dict
		@return: The current player state to JSON serializable representation.
		"""
		state = { 'type':'Player',
				  'alive':self.alive,
				  'name':self.name,
				  'id': id(self),
				  'score': self.score,
				  'resources': self.resources,
				  'ships': self.ships.keys(),
				  'bases': self.bases.keys(),
				  'refineries': self.refineries.keys()
				  }
		return state
	
	def forfeit(self):
		"""
		Deactivate the player.
		"""
		self.alive = False

class PlayerTests(unittest.TestCase):
	def test_create(self):
		p = Player("Hello","world")
		self.assertTrue(p.name == "Hello")
		self.assertTrue(p.auth == "world")
		self.assertTrue(p.alive)
		self.assertTrue(len(p.objects) == 0)

	def test_add(self):
		p = Player("a","b")
		objects = []
		objects.append("hello")
		objects.append("test")
		for i in objects:
			p.add_object(i)
		self.assertTrue(len(p.objects) == 2)

	def test_forfeit(self):
		p = Player("a","b")
		p.forfeit()
		self.assertFalse(p.alive)


if __name__ == "__main__":
	unittest.main()
