import unittest
import mm18.game.constants
from mm18.game.tower import Tower
from mm18.game.units import Unit
from mm18.game.board import Board
from mm18.game.player import Player

"""Tests for the game code go here"""
class TestGame(unittest.TestCase):

	"""Player tests"""
#1
	def testInvalidPlayerCreate1(self):
		test = Player(1)
		self.assertRaises(TypeError)
#2
	def testInvalidPlayerCreate2(self):
		test = Player('a')
		self.assertRaises(TypeError)
#3
	def testInvalidPlayerCreate3(self):
		with self.assertRaises(NameError):
			test = Player(false)
#4
	def testValidPlayerCreate(self):
		test = Player("testName")
		self.assertEqual(test.name, "testName")
		self.assertEqual(test.resources, mm18.game.constants.BASE_RESOURCES)
		self.assertEqual(test.allowedUpgrade, 0)
		self.assertEqual(test.sentUnits, 0)
#5
	def testInvalidPlayerUpgrade(self):
		test = Player("testName")
		self.assertFalse(test.increaseUpgrade())
#6
	def testInvalidPlayerUpgrade1(self):
		test = Player("testName")
		with self.assertRaises(TypeError):
			test.increaseUpgrade(5)
#7
	def testValidPlayerUpgrade(self):
		test = Player("testName")
		test.sentUnits = mm18.game.constants.UPGRADE_INCREASE*(test.allowedUpgrade+1)+1
		self.assertTrue(test.increaseUpgrade())
#8
	def testInvalidPlayerPurchase(self):
		test = Player("testName")
		self.assertFalse(test.purchaseCheck(test.resources + 1))
#9
	def testInvalidPlayerPurchase1(self):
		test = Player("testName")
		with self.assertRaises(AssertionError):
			test.purchaseCheck("I want to buy a cat")
#10
	def testValidPlayerPurchase(self):
		test = Player("testName")
		self.assertTrue(test.purchaseCheck(test.resources - 1))
		test.purchase(test.resources - 1)
		self.assertEquals(test.resources,1)

	"""Board Tests"""
#11
	def testInvalidBoardCreation(self):
		with self.assertRaises(TypeError):
			test = Board(1)
#12
	def testValidBoardCreation(self):
		test = Board()
		self.assertEquals(len(test.board),0)
#13
	def testInvalidPosition(self):
		test = Board()
		self.assertFalse(test.validPosition((mm18.game.constants.BOARD_SIDE,mm18.game.constants.BOARD_SIDE)))
#14
	def testInvalidPosition1(self):
		test = Board()
		self.assertFalse(test.validPosition((-1,-1)))
#15
	def testInvalidPosition2(self):
		test = Board()
		self.assertFalse(test.validPosition((2,-1)))
#16
	def testInvalidPosition3(self):
		test = Board()
		with self.assertRaises(TypeError):
			test.validPosition(5)
#17
	def testValidPosition(self):
		test = Board()
		self.assertTrue(test.validPosition((0,0)))
#18
	def testInvalidAddItem(self):
		test = Board()
		with self.assertRaises(TypeError):
			test.addItem("meow")
#19
	def testInvalidAddItem1(self):
		test = Board()
		self.assertFalse(test.addItem("meow",(0,-1)))
#20
	def testValidAddItem(self):
		test = Board()
		testPlayer = Player("testName")
		test.addItem(testPlayer,(0,0))
		self.assertEquals(test.board[(0,0)],testPlayer)
#21
	def testInvalidGetItem(self):
		pass


if __name__ == "__main__":
	unittest.main()
