import pyglet
from pyglet.gl import *

from mm18.game.board import Board

class Visualizer:
	def __init__(self, board):
		self.board = board
		self.window = pyglet.window.Window()
		self.window.set_handler('on_draw', self.onDraw)
		glClearColor(1, 1, 1, 1)

	def onDraw(self):
		self.window.clear()

	def run(self):
		pyglet.app.run()
