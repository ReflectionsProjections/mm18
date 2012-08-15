import unittest
import mm18.game.constants
from mm18.game.tower import Tower
from mm18.game.units import Unit
from mm18.game.board import Board
from mm18.game.player import Player

"""Tests for the game code go here"""
class TestGame(unittest.TestCase):

	def setUp(self):
		unittest.TestCase.setUp(self)
		self.testPlayer = Player("testName")
		self.testBoard = Board()

	def tearDown(self):
		unittest.TestCase.tearDown(self)

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
		self.assertEqual(self.testPlayer.name, "testName")
		self.assertEqual(self.testPlayer.resources, mm18.game.constants.BASE_RESOURCES)
		self.assertEqual(self.testPlayer.allowedUpgrade, 0)
		self.assertEqual(self.testPlayer.sentUnits, 0)
#5
	def testInvalidPlayerUpgrade(self):
		self.assertFalse(self.testPlayer.increaseUpgrade())
#6
	def testInvalidPlayerUpgrade1(self):
		with self.assertRaises(TypeError):
			self.testPlayer.increaseUpgrade(5)
#7
	def testValidPlayerUpgrade(self):
		self.testPlayer.sentUnits = mm18.game.constants.UPGRADE_INCREASE*(self.testPlayer.allowedUpgrade+1)+1
		self.assertTrue(self.testPlayer.increaseUpgrade())
#8
	def testInvalidPlayerPurchase(self):
		self.assertFalse(self.testPlayer.purchaseCheck(self.testPlayer.resources + 1))
#9
	def testInvalidPlayerPurchase1(self):
		with self.assertRaises(AssertionError):
			self.testPlayer.purchaseCheck("I want to buy a cat")
#10
	def testValidPlayerPurchase(self):
		self.assertTrue(self.testPlayer.purchaseCheck(self.testPlayer.resources - 1))
		self.testPlayer.purchase(self.testPlayer.resources - 1)
		self.assertEquals(self.testPlayer.resources,1)

	"""Board Tests"""
#11
	def testInvalidBoardCreation(self):
		with self.assertRaises(TypeError):
			test = Board(1)
#12
	def testValidBoardCreation(self):
		self.assertEquals(len(self.testBoard.board),0)
#13
	def testInvalidPosition(self):
		self.assertFalse(self.testBoard.validPosition((mm18.game.constants.BOARD_SIDE,mm18.game.constants.BOARD_SIDE)))
#14
	def testInvalidPosition1(self):
		self.assertFalse(self.testBoard.validPosition((-1,-1)))
#15
	def testInvalidPosition2(self):
		self.assertFalse(self.testBoard.validPosition((2,-1)))
#16
	def testInvalidPosition3(self):
		with self.assertRaises(TypeError):
			self.testBoard.validPosition(5)
#17
	def testValidPosition(self):
		self.assertTrue(self.testBoard.validPosition((0,0)))
#18
	def testInvalidAddItem(self):
		with self.assertRaises(TypeError):
			self.testBoard.addItem("meow")
#19
	def testInvalidAddItem1(self):
		self.assertFalse(self.testBoard.addItem("meow",(0,-1)))
#20
	def testValidAddItem(self):
		self.testBoard.addItem(self.testPlayer,(0,0))
		self.assertEquals(self.testBoard.board[(0,0)],self.testPlayer)
#21
	def testValidGetItem(self):
		self.assertEquals(self.testBoard.getItem((0,1)),None)
#22
	def testValidRemoveItem(self):
		self.testBoard.addItem(self.testPlayer,(0,0))
		self.testBoard.board[(0,0)]
		self.testBoard.removeItem((0,0))
		with self.assertRaises(KeyError):
			self.testBoard.board[(0,0)]

	"""Unit Tests"""
#23
	#Not enough resources
	def testInvalidPurchaseUnit(self):
		self.testPlayer.resources = 0
		test = Unit.purchaseUnit(0,0,self.testPlayer)
		self.assertEquals(test,None)
#24
	#Level too high
	def testInvalidPurchaseUnit1(self):
		test = Unit.purchaseUnit(3,0,self.testPlayer)
		self.assertEquals(test,None)
#25
	#Invalid spec
	def testInvalidPurchaseUnit2(self):
		test = Unit.purchaseUnit(0,-2,self.testPlayer)
		self.assertEquals(test, None)
		test = Unit.purchaseUnit(0,2,self.testPlayer)
		self.assertEquals(test, None)
#26
	def testValidPurchaseUnit(self):
		testUnit = Unit.purchaseUnit(0,1,self.testPlayer)
		self.assertEquals(testUnit.level,0)
		self.assertEquals(testUnit.specialisation,1)
		self.assertEquals(testUnit.owner, self.testPlayer.name)

	"""Tower Tests"""

	def testInvalidPurchaseTower(self):
		pass



"""Uncomment & delete this line for concise test output
if __name__ == "__main__":
	unittest.main()
"""
suite = unittest.TestLoader().loadTestsFromTestCase(TestGame)
unittest.TextTestRunner(verbosity=2).run(suite)
