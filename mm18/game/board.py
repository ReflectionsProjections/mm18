#! /usr/bin/env python

import constants
import json
from collections import deque

"""
This is the board class.
It is where the code for the board goes.
"""

class Board:
	
	"""
	Board class. 
	The board consists of two lists and a dictionary.  The dictionary contains the locations of the towers (key is a tuple for location on the board, entry is a tower object).  The base list contains the tuple locations of the base - unordered.   The path list contains the tuple locations of the path, ordered starting with those closest to the base and working outwards.

	base -- a list of tuples that represent the base location
	path -- a list of tuples that represent the path locations (ordered in findPaths method)
	"""
	def __init__(self, base, path):
		self.base = base
		self.path = path
		self.tower = {}

	"""
	Reads in json for the board layout from a file and sorts it into two lists - for base positions and path positions
	"""
	@staticmethod
	def jsonLoad():
		data =json.load(open(board1.json).read())
		bases = data['bases']
		baseList = [tuple(pair) for pair in bases]
		paths = data['paths']
		pathList = [tuple(pair) for pair in paths]
		findPaths(baseList, pathList)


	"""
	Breadth-first search method that takes the unordered list of path locations and sorts them by how far from the base they are.

	baseList -- a list that contains the base locations
	pathList -- a list that contains the paths to the base in no order
	"""
	@staticmethod
	def findPaths(baseList, pathList):
		pathQueue = deque(baseList)
		outPath = []
		for elem in pathQueue:
			if (x,y) not in outPath:
				x,y = pathQueue.popleft()
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
		Board(baseList,outPath)

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




