#! /usr/bin/env python

import constants

"""
This is the board class.
It is where the code for the board goes.
As far as I understand each player has their own board.
The board needs:
	-a map
	-Ability to add/delete things from the map
"""

class Board:
	
	"""
	Board class. 
	The board is made here in the form of a dictionary with each key being a tuple that corresponds the location and the entry being a reference to the item at that that location.
	"""
	def __init__(self):
		self.board = {}

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
		if self.validPosition(position) and self.getItem(position) == None:
			self.board[position] = item
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
		return self.board.get(position,None)

	"""
	Removes the item at the position

	position -- a tuple containing object position
	"""
	def removeItem(self, position):
		if self.getItem(position) != None:
			del self.board[position]




