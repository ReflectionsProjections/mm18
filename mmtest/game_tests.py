import unittest
import mm18.game.constants
from mm18.game.tower import Tower
from mm18.game.units import Unit
from mm18.game.board import Board
from mm18.game.player import Player

"""Tests for the game code go here"""
class TestGame(unittest.TestCase):

	"""Player tests"""
	def testInvalidPlayerCreate1(self):
		test = Player(1)
		self.assertRaises(TypeError)

	def testInvalidPlayerCreate2(self):
		test = Player('a')
		self.assertRaises(TypeError)

	def testInvalidPlayerCreate3(self):
		try:
			test = Player(false)
		except NameError:
			pass
		else:
			fail("Expected a NameError")

	def testValidPlayerCreate(self):
		test = Player("testName")
		self.assertEqual(test.name, "testName")
		self.assertEqual(test.resources, mm18.game.constants.BASE_RESOURCES)
		self.assertEqual(test.allowedUpgrade, 0)
		self.assertEqual(test.sentUnits, 0)

	def testInvalidPlayerUpgrade(self):
		test = Player("testName")
		self.assertFalse(test.increaseUpgrade())

	def testValidPlayerUpgrade(self):
		test = Player("testName")
		test.sentUnits = mm18.game.constants.UPGRADE_INCREASE*(test.allowedUpgrade+1)+1
		self.assertTrue(test.increaseUpgrade())

	"""Board Tests"""


if __name__ == "__main__":
	unittest.main()
