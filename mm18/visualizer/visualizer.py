import os
import pyglet
from pyglet.gl import *

from mm18.game.board import Board
from mm18.game.constants import BOARD_SIDE

resources_path = os.path.join(os.path.dirname(__file__), 'resources')
pyglet.resource.path.append(resources_path)
pyglet.resource.reindex()

tex_terrain = pyglet.resource.image('genericGrass.png')
tex_path = pyglet.resource.image('genericPath.png')

class Visualizer:

	def __init__(self, board):
		self.board = board
		self.window = pyglet.window.Window(32*BOARD_SIDE, 32*BOARD_SIDE)
		self.window.set_handler('on_draw', self.onDraw)
		glClearColor(1, 1, 1, 1)

	def onDraw(self):
		self.window.clear()
		tiles = ((x, y) for x in range(BOARD_SIDE) for y in range(BOARD_SIDE))
		for (x, y) in tiles:
			tex = tex_path if (x, y) in self.board.path else tex_terrain
			tex.blit(32 * x, 32 * y)

	def run(self):
		pyglet.app.run()
