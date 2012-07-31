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
		with self.assertRaises(NameError):
			test = Player(false)

	def testValidPlayerCreate(self):
		test = Player("testName")
		self.assertEqual(test.name, "testName")
		self.assertEqual(test.resources, mm18.game.constants.BASE_RESOURCES)
		self.assertEqual(test.allowedUpgrade, 0)
		self.assertEqual(test.sentUnits, 0)

	def testInvalidPlayerUpgrade(self):
		test = Player("testName")
		self.assertFalse(test.increaseUpgrade())

	def testInvalidPlayerUpgrade1(self):
		test = Player("testName")
		with self.assertRaises(TypeError):
			test.increaseUpgrade(5)

	def testValidPlayerUpgrade(self):
		test = Player("testName")
		test.sentUnits = mm18.game.constants.UPGRADE_INCREASE*(test.allowedUpgrade+1)+1
		self.assertTrue(test.increaseUpgrade())

	def testInvalidPlayerPurchase(self):
		test = Player("testName")
		self.assertFalse(test.purchaseCheck(test.resources + 1))

	def testInvalidPlayerPurchase1(self):
		test = Player("testName")
		with self.assertRaises(AssertionError):
			test.purchaseCheck("I want to buy a cat")

	def testValidPlayerPurchase(self):
		test = Player("testName")
		self.assertTrue(test.purchaseCheck(test.resources - 1))
		test.purchase(test.resources - 1)
		self.assertEquals(test.resources,1)

	"""Board Tests"""


if __name__ == "__main__":
	unittest.main()
