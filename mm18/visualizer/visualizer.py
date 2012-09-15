import os
import pyglet
from pyglet.gl import *

from mm18.game import constants
from mm18.game.board import Board

TILE_SIZE = 32

resources_path = os.path.join(os.path.dirname(__file__), 'resources')
pyglet.resource.path.append(resources_path)
pyglet.resource.reindex()

tex_terrain = pyglet.resource.image('genericGrass.png')
tex_path = pyglet.resource.image('genericPath.png')

class Visualizer:

	def __init__(self, board):
		self.board = board
		self.window = pyglet.window.Window(
			width=TILE_SIZE * constants.BOARD_SIDE,
			height=TILE_SIZE * constants.BOARD_SIDE,
		)
		self.window.set_handler('on_draw', self.draw)
		pyglet.clock.schedule_interval(self.update, 1)
		glClearColor(1, 1, 1, 1)

	def update(self, dt=0):
		# parse and perform commands from log
		# advance the game controller
		pass

	def draw(self):
		self.window.clear()
		self.drawBoard(self.board)

	def drawBoard(self, board):
		width = height = constants.BOARD_SIDE
		tiles = ((x, y) for x in range(width) for y in range(height))
		for (x, y) in tiles:
			tex = tex_path if (x, y) in self.board.path else tex_terrain
			tex.blit(
				x=TILE_SIZE * x,
				y=TILE_SIZE * y,
				width=TILE_SIZE,
				height=TILE_SIZE,
			)

	def run(self):
		pyglet.app.run()
