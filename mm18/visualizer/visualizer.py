import os
import pyglet
from pyglet.gl import *
from pyglet import image

from mm18.game.board import Board
from mm18.game.constants import BOARD_SIDE

class Visualizer:
	resourcesPath = os.path.join(os.path.dirname(__file__), 'resources')
	pyglet.resource.path.append(resourcesPath)
	pyglet.resource.reindex()

	texTerrain = pyglet.resource.image('genericGrass.png')
	texPath = pyglet.resource.image('genericPath.png')

	def __init__(self, board):
		self.board = board
		self.window = pyglet.window.Window(32*BOARD_SIDE, 32*BOARD_SIDE)
		self.window.set_handler('on_draw', self.onDraw)
		glClearColor(1, 1, 1, 1)

	def onDraw(self):
		self.window.clear()
		for x in range(BOARD_SIDE):
			for y in range(BOARD_SIDE):
				self.texTerrain.blit(x*32,y*32)
		path=self.board.path
		for block in path:
			self.texPath.blit(block[0]*32, block[1]*32)

	def run(self):
		pyglet.app.run()
