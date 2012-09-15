#! /usr/bin/env python

import constants
import json
import os
from collections import deque
from collections import defaultdict


"""
This is the board class.
It is where the code for the board goes.
"""

class Board:

	"""
	Board class. 
	The board consists of two lists and a dictionary.  The dictionary contains the locations of the towers (key is a tuple for location on the board, entry is a tower object).  The base list contains the tuple locations of the base - unordered.   The path list contains the tuple locations of the path, ordered starting with those closest to the base and working outwards.

	base -- a list of tuples that represent the base location
	path -- a list of tuples that represent the path locations (ordered in orderPathsByClosest method)
	"""
	def __init__(self, base, path):
		self.width = constants.BOARD_SIDE
		self.height = constants.BOARD_SIDE
		self.base = base
		self.path = path
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

	"""
	Reads in json for the board layout from a file and sorts it into two lists one for base positions and the other for path positions
	"""
	@staticmethod
	def jsonLoad(filename):
		filePath = os.path.join(os.path.dirname(__file__), filename)
		data =json.load(open(filePath))
		bases = data['bases']
		baseList = [tuple(pair) for pair in bases]
		paths = data['paths']
		pathList = [tuple(pair) for pair in paths]
		return Board.orderPathsByClosest(baseList, pathList)


	"""
	Breadth-first search method that takes the unordered list of path locations and sorts them by how far from the base they are.

	baseList -- a list that contains the base locations
	pathList -- a list that contains the paths to the base in no order
	"""
	@staticmethod
	def orderPathsByClosest(baseList, pathList):
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
		return Board(baseList,outPath)

	"""
	Depth-first search method that uses a list of path locations to build a
	list of paths, where each path starts at a starting path square (on the
	edge of the board) and ends at the base.
	"""
	# TODO: make sure that paths end at a base
	def findPaths(self):
		paths = []
		
		pathStack = [self.startPos[constants.NORTH]]
		paths = self.findPathsRecurse(pathStack, paths)

		pathStack = [self.startPos[constants.EAST]]
		paths = self.findPathsRecurse(pathStack, paths)
			
		pathStack = [self.startPos[constants.SOUTH]]
		paths = self.findPathsRecurse(pathStack, paths)

		pathStack = [self.startPos[constants.WEST]]
		paths = self.findPathsRecurse(pathStack, paths)

		return paths
	
	"""
	The helper function to findPaths, it actually travels down the paths via a
	depth first search and adds a completed path the the paths list when it
	cannot go any farther.
	"""
	def findPathsRecurse(self, pathStack, paths):
		print "\n"
		print pathStack
		
		pathEnds = True
		x,y = pathStack[len(pathStack) - 1]
		
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



	"""
	Check whether the position of the object being inserted is a valid placement on the board.
	Will contain error handling for invalid positions.

	position -- tuple containing object position
	"""
	def validPosition(self, position):
		x,y=position
		return x >= 0 and y >=0 and x < constants.BOARD_SIDE and y < constants.BOARD_SIDE

	"""
	Adds an object to the board provided nothing is already in the location.
	Returns true if successful and false if not

	item -- an object, most likely a tower
	position -- a tuple for the position of the object
	"""
	def addItem(self, item, position):
		if self.validPosition(position) and self.getItem(position) == None and position not in self.base and position not in self.path:
			self.tower[position] = item
			return True
		else:
			return False

	"""
	Gets the item at the position or returns none if no object exists.
	Will contain error handling for something?
	If no error handling is needed class is unecessary and can be replaced just by the dict.get method.

	position -- a tuple containing object position
	"""
	def getItem(self, position):
		return self.tower.get(position,None)

	"""
	Removes the item at the position

	position -- a tuple containing object position
	"""
	def removeItem(self, position):
		if self.getItem(position) != None:
			del self.tower[position]


	"""
	Adds a tower to all the appropriate places of the hitList

	self -- the board
	tower -- the tower to add to the hitList
	"""
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
	

	"""
	Removes a certain tower from all places of the hitlist

	self -- the board
	tower -- the tower to be removed
	"""

	def removeFromHitList(self, tower):
		for elem, i in self.hitList.iteritems():
			for i in self.hitList[elem]:
				i.remove(tower)
			
		

