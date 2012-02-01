#! /usr/bin/env python
from math import hypot
import unittest
from vector import distance
import Constants
from map_obj import MapObject
from ship import Ship
class Planet(MapObject):
	"""
	A planet that can be captured. A base can be built here by a ship.
	"""

	def __init__(self, position, size):
		"""
		Construct a planet.

		@type  position: tuple
		@param position: Position of Planet on the map

		@type  size: int
		@param size: Size of the Planet
		"""
		super(Planet, self).__init__(position)

		self.size = size
		# will contain refrence to base if it contains one
		self.base = None

	def to_dict(self):
		"""
		Return the current state in JSON serializable representation.

		@type: dict
		@return The current game state in JSON serializable representation.
		"""
		state = {'type': 'Planet',
				 'id': id(self),
				 'position': self.position,
				 'size':self.size,
				 'base': self.base.to_dict() if self.base else None
				}
		return state

class Base(object):
	"""
	A base that can be built on a planet.  Players can use these to
	create ships, etc.
	"""

	def __init__(self, planet, owner):
		"""
		Construct a base.

		@type planet: Planet object
		@param planet: The Planet object that this base is associated with
		
		@type owner: Player object
		@param owner: The Player object this base is owned by
		"""
		self.built = Constants.base_build_time
		self.alive = True
		self.planet = planet
		self.owner = owner
		self.position = self.planet.position
		self.max_health = Constants.base_health
		self.health = self.max_health
		self.events = []
		self.busy = 0
		owner.add_object(self)
		self.planet.base = self
		# holds all events to be processed on turn handle
		self.events = []

		# holds results from turns to be returned to user
		# dict of lists accessed like results[turn]
		self.results = {0: []}

		# set methods used to true in this dict to prevent
		# double dipping
		self.methods_used = {}
		self.current_action = None
		owner.add_object(self)


	def create_ship(self, position):
		"""
		Construct a ship.
		
		@type: tuple
		@param position: location the player wants the object at
		"""
		# if outside build radius, move position in
		if distance(self.planet.position, position) > Constants.build_radius:
			mag = hypot(*position)
			position = (position[0]*(Constants.build_radius/mag),
						position[1]*(Constants.build_radius/mag))
		new_ship = Ship(position, self.owner)
		self.owner.resources -= Constants.ship_price
		return new_ship

	def salvage_ship(self, ship_id):
		"""
		Salvage a ship, reimbursing you with some of your resources.

		@type ship: Ship object
		@param ship: A ship object to delete within the salvage_radius
		"""		
		from game_instance import game
		ship = game.game_map.ships[ship_id]
		resources = (float(ship.health)/Constants.ship_health)*\
			Constants.salvage_multiplier
		ship._delete()
		self.owner.resources += resources

	def repair_ship(self, ship_id):
		"""
		Repair a ship, adding repair_percent ship health per turn used.
		
		@type ship: Ship object
		@param ship: A ship object to add health to
		"""
		from game_instance import game
		ship = game.game_map.ships[ship_id]
		if distance(self.position, ship.position) < Constants.base_repair_radius:
			ship.health += Constants.repair_percent * Constants.ship_health
			if ship.health > Constants.ship_health:
				ship.health = Constants.ship_health

	def destroy(self):
		"""
		Removes a base from the planet and owner refrences
		"""
		self._delete()

	def _delete(self):
		"""Delete object from map dicts and owner dicts.

		@type  object: Base object
		@param object: object to delete from map and owner dicts
		"""
		self.planet.base = None
		del self.owner.objects[id(self)]
		del self.owner.bases[id(self)]


	def to_dict(self):
		"""
		Return the current state in JSON serializable representation.

		@type: dict
		@return: The current base state in JSON serializable representation.
		"""
		state = { 'type':'Base',
				  'id': id(self),
				  'built': self.built,
				  'busy':self.busy,
				  'position': self.position,
				  'planet':id(self.planet),
				  'owner': id(self.owner),
				  'health': self.health,
				  'max_health': self.max_health,
				  'events':self.events
				  }
		return state

	
if __name__ == '__main__':
	unittest.main()
 
