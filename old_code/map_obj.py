#! /usr/bin/env python

import unittest

from game_instance import game

class MapObject(object):
	"""
	Base class for all game objects on the map since they need
	certain common info
	"""

	def __init__(self, position):
		"""
		Initializes map object

		@type  position: tuple
		@param position: Position of the GameObject on the map
		"""

		self.position = position
		self.velocity = (0,0)
		self.direction = 0
		self.size = 1

		# holds all events to be processed on turn handle
		self.events = []

		# holds results from turns to be returned to user
		# dict of lists accessed like results[turn]
		self.results = {0: []}

		# set methods used to true in this dict to prevent
		# double dipping
		self.methods_used = {}

		# Add this object to the game map
		game.game_map.add_object(self)


	def step(self, dt):
		"""Timestep executed every turn.

		@type  dt: number
		@param dt: Change in time
		"""

		vx, vy = self.velocity
		x, y = self.position
		self.position = (x + dt*vx, y + dt*vy)

	def handle_damage(self, damage_event):
		"""
		By default, do nothing.

		@type  damage_event: dict
		@param damage_event: Whatever damage_events are
		"""

		pass

	def _to_dict(self):
		"""
		Returns the current state in JSON serializable representation.
		@return: The current game state in JSON serializable representation
		"""

		from game_instance import game

		state = {'obj_id': id(self),
				'position':self.position,
				'results':self.results[game.turn]
				}
		return state


	def _delete(self):
		"""Delete object from map dicts and owner dicts.

		@type  object: MapObject object
		@param object: object to delete from map and owner dicts
		"""

		from game_instance import game

		for dict in game.game_map.dicts:
			if id(self) in dict.keys():
				del dict[id(self)]
		if hasattr(self, 'owner'):
			owner = self.owner
			for dict in owner.dicts:
				if id(self) in dict.keys():
					del dict[id(self)]

if __name__=='__main__':
	unittest.main()
