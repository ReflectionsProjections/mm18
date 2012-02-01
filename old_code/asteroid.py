#! /usr/bin/env python
from game_instance import game
from map_obj import MapObject
import Constants
import unittest

class Asteroid(MapObject):
	"""
	An asteroid that a refinery can be built on
	"""
	def __init__(self, position, size):
		"""
		Construct an asteroid.
		
		@type  position: tuple
		@param position: Position of Asteroid on the map.
		
		@type  size: int
		@param size: Size of the Asteroid
		"""
		super(Asteroid, self).__init__(position)
		self.size = size
		self.resources = size * Constants.asteroid_scale
		self.refinery = None
		self.events = []

	def pull_resources(self):
		"""
		Remove a constant amount of resources from the asteroid.
		"""
		self.resources -= Constants.resource_pull
		if self.resources <= 0:
			if self.refinery:
				del refinery.owner.refineries[id(self)]
			self._delete()

	def to_dict(self):
		"""
		Return the current state in JSON serializable representation.

		@type: dict
		@return The current game state in JSON serializable representation.
		"""
		state = {'type':'Asteroid',
				 'id': id(self),
				 'position': self.position,
				 'resources' : self.resources,
				 'size' : self.size,
				 'refinery' : self.refinery.to_dict() if self.refinery else None
				 }
		return state

class Refinery(object):

	def __init__(self, asteroid, owner):
		"""
		Creates a refinery.
		"""
		self.asteroid = asteroid
		self.owner = owner
		self.built = 5
		self.position = asteroid.position
		self.max_health = Constants.refinery_health
		self.health = self.max_health
		# holds all events to be processed on turn handle
		self.events = []

		# holds results from turns to be returned to user
		# dict of lists accessed like results[turn]
		self.results = {0: []}

		# set methods used to true in this dict to prevent
		# double dipping
		self.methods_used = {}
		asteroid.refinery = self
		owner.add_object(self)


	def to_dict(self):
		"""
		Return the current state in JSON serializable representation.

		@type: dict
		@return The current refinery state in JSON serializable representation.
		"""
		state = { 'type':'Refinery',
				  'id': id(self),
				  'built': self.built,
				  'owner': id(self.owner),
				  'position':self.asteroid.position,
				  'asteroid':id(self.asteroid),
				  'max_health':self.max_health,
				  'health':self.health,
				  'events':self.events
				  }
		return state

	def destroy(self):
		"""
		Removes a refinery from the planet and owner refrences
		"""
		self._delete()

	def _delete(self):
		"""Delete object from map dicts and owner dicts.

		@type  object: Base object
		@param object: object to delete from map and owner dicts
		"""
		self.asteroid.refinery = None
		del self.owner.objects[id(self)]
		del self.owner.refineries[id(self)]


if __name__ == '__main__':
	unittest.main()
