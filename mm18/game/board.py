#! /usr/bin/env python

import constants
import json
import os
from collections import deque, defaultdict
from path import Path
import itertools

## @file board.py


## This is the board class.
#  It is where the code for the board goes.
class Board:

	## Board class. 
	#  The board consists of two lists and a dictionary.
	#  The dictionary contains the locations of the towers
	#  (key is a tuple for location on the board, entry is a tower object).
	#  The base list contains the tuple locations of the base - unordered.
	#  The path list contains the tuple locations of the path,
	#  ordered starting with those closest to the base and working outwards.
	#  @param base A list of tuples that represent the base location
	#  @param path A list of tuples that represent the path locations (ordered in orderPathsByClosest method)
	#  @param width An optional arguement, the width of the board
	#  @param height An optional arguement, the height of the board
	def __init__(self, base, path, width=constants.BOARD_SIDE, height=constants.BOARD_SIDE):
		self.base = base
		self.path = self.orderPathSquaresByClosest(base, path)
		
		self.width = width
		self.height = height
		
		self.tower = {}
		self.hitList = defaultdict(list)

		self.startPos = 4*[None]
		for x,y in self.path:
			if y is 0:
				self.startPos[constants.NORTH] = (x,y)
			elif x is self.width - 1:
				self.startPos[constants.EAST] = (x,y)
			elif y is self.height - 1:
				self.startPos[constants.SOUTH] = (x,y)
			elif x is 0:
				self.startPos[constants.WEST] = (x,y)

		pathList = self.findPaths()
		self.paths = {direction: Path(pathList[direction]) \
			for direction in constants.DIRECTIONS}
		

	## Reads in json for the board layout from a file and sorts it into two lists
	#  one for base positions and the other for path positions
	@staticmethod
	def jsonLoad(filename):
		filePath = os.path.join(os.path.dirname(__file__), filename)
		data =json.load(open(filePath))
		
		bases = data['bases']
		baseList = [tuple(pair) for pair in bases]
		
		paths = data['paths']
		pathList = [tuple(pair) for pair in paths]
		
		width = data['width']
		height = data['height']

		return Board(baseList, pathList)

	## Breadth-first search method that takes the unordered list of path locations
	#  and sorts them by how far from the base they are.
	#  @param baseList A list that contains the base locations
	#  @param pathList A list that contains the paths to the base in no order
	def orderPathSquaresByClosest(self, baseList, pathList):
		pathQueue = deque(baseList)
		outPath = []
		while pathQueue:
			x,y = pathQueue.popleft()
			if (x,y) not in outPath:
				if (x, y + 1) in pathList:
					pathQueue.append((x, y + 1))
				if (x, y - 1) in pathList:
					pathQueue.append((x, y - 1))
				if (x + 1, y) in pathList:
					pathQueue.append((x + 1, y))
				if (x - 1, y) in pathList:
					pathQueue.append((x - 1, y))
				if (x,y) not in baseList:
					outPath.append((x,y))
		return outPath

	## Depth-first search method that uses a list of path locations to build a
	#  list of paths, where each path starts at a starting path square (on the
	#  edge of the board) and ends at the base.
	#  TODO: make sure that paths end at a base
	def findPaths(self):
		paths = []
		
		northStack = self.startPos[constants.NORTH]
		eastStack = self.startPos[constants.EAST]
		southStack = self.startPos[constants.SOUTH]
		westStack = self.startPos[constants.WEST]
		
		if northStack:
			paths.append(self.findPathsRecurse([northStack],paths))
		else:
			paths.append(None)
		if eastStack:
			paths.append(self.findPathsRecurse([eastStack],paths))
		else:
			paths.append(None)
		if southStack:
			paths.append(self.findPathsRecurse([southStack],paths))
		else:
			paths.append(None)
		if westStack:
			paths.append(self.findPathsRecurse([westStack],paths))
		else:
			paths.append(None)

		return paths
	
	## The helper function to findPaths, it actually travels down the paths via a
	#  depth first search and adds a completed path the the paths list when it
	#  cannot go any farther.
	def findPathsRecurse(self, pathStack, paths):
		pathEnds = True
		x,y = pathStack[-1]
		
		north = (x, y+1)
		if north not in pathStack and north in self.path:
			pathEnds = False
			pathStack.append(north)
			self.findPathsRecurse(pathStack, paths)

		east = (x+1, y)
		if east not in pathStack and east in self.path:
			pathEnds = False
			pathStack.append(east)
			self.findPathsRecurse(pathStack, paths)
		
		south = (x, y-1)
		if south not in pathStack and south in self.path:
			pathEnds = False
			pathStack.append(south)
			self.findPathsRecurse(pathStack, paths)
		
		west = (x-1, y)
		if west not in pathStack and west in self.path:
			pathEnds = False
			pathStack.append(west)
			self.findPathsRecurse(pathStack, paths)
		
		if pathEnds:
			paths.append(pathStack[:])
		
		pathStack.pop()
		return paths

	## Check whether the position of the object being inserted is a valid placement on the board.
	#  Will contain error handling for invalid positions.
	#  @param position Tuple containing object position
	# TODO: Error handling for invalid positions
	def validPosition(self, position):
		x,y=position
		return x >= 0 and y >=0 and x < constants.BOARD_SIDE and y < constants.BOARD_SIDE

	## Adds an object to the board provided nothing is already in the location.
	#  @return true if successful and false if not
	#  @param item An object, most likely a tower
	#  @param position A tuple for the position of the object
	def addItem(self, item, position):
		if self.validPosition(position) and self.getItem(position) == None and position not in self.base and position not in self.path:
			self.tower[position] = item
			return True
		else:
			return False

	## Gets the item at the position or returns none if no object exists.
	#  Will contain error handling for something?
	#  If no error handling is needed class is unecessary and can be replaced just by the dict.get method.
	#  @return Item at the position or none if no object exists
	#  @param position A tuple containing object position
	def getItem(self, position):
		return self.tower.get(position,None)

	## Removes the item at the position
	#  @param position A tuple containing object position
	def removeItem(self, position):
		if self.getItem(position) != None:
			del self.tower[position]

	## Adds a tower to all the appropriate places of the hitList
	#  @param self The board
	#  @param tower The tower to add to the hitList
	def addToHitList(self, tower, position):
		tX, tY = position
		tXLower = tX - constants.TOWER_RANGE[tower.upgrade]
		if tXLower < 0:
			tXLower = 0
		tXUpper = tX + constants.TOWER_RANGE[tower.upgrade]
		if tXUpper >= constants.BOARD_SIDE:
			txUpper = constants.BOARD_SIDE - 1
		tYLower = tY - constants.TOWER_RANGE[tower.upgrade]
		if tYLower < 0:
			tYLower = 0
		tYUpper = tY + constants.TOWER_RANGE[tower.upgrade]
		if tYUpper >= constants.BOARD_SIDE:
			tYUpper = constants.BOARD_SIDE - 1
		for elem in self.path:
			elemX, elemY = elem
			if elemX >= tXLower and elemX <= tXUpper:
				if elemY >= tYLower and elemY <= tYUpper:
					self.hitList[elem].append(tower)

	## Removes a certain tower from all places of the hitlist
	#  @param self The board
	#  @param tower The tower to be removed
	def removeFromHitList(self, tower):
		for elem, i in self.hitList.iteritems():
			for i in self.hitList[elem]:
				i.remove(tower)
	
	## Goes through the paths, and if there is an enemy unit, attack it.
	#  @param self The board
	def fireTowers(self):
		used = set()
		for unit, pos in self.units():
			for tower in self.hitlist[pos]:
				if unit.health <= 0:
					break
				if tower not in used:
					used.add(tower)
					tower.fire(unit)

	## Queue's the unit at the entrance of the path it is supposed to take.
	#  @param unit The unit being placed
	#  @param q Which entrance the unit needs to go to
	def queueUnit(self, unit, q):
		if q in self.paths:
			if self.paths[q].moving is not None:
				self.paths[q].start(unit)
				return True
		return False

	## Return a generator of pairs of unit and position on the board,
	#  in order of increasing distance from the base
	def units(self):
		paths = [self.paths[q] for q in
				 [constants.NORTH,constants.EAST,constants.SOUTH,constants.WEST]]
		return ((unit,pos) for front in itertools.izip()
	                     for (unit,pos) in front
						 if unit is not None and unit.health > 0)


	## Advance the board state.
	#  Incoming units move forward, ones reaching the base do damage
	# TODO: check if next to base before exploding, dead units die
	def moveUnits(self):
		for path in self.paths.itervalues():
			unit = path.advance()
		#	if unit is not None and unit.health > 0:
		#		self.owner.damage(unit.finalDamage())

	## Return the tower list
	def getTowers(self):
		return tower
