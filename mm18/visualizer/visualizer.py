import os
import pyglet
from pyglet.gl import *

from mm18.game.board import Board

class Visualizer:
	resourcesPath = os.path.join(os.path.dirname(__file__), 'resources')
	pyglet.resource.path.append(resourcesPath)
	pyglet.resource.reindex()

	texTerrain = pyglet.resource.image('genericGrass.png')
	texPath = pyglet.resource.image('genericPath.png')

	def __init__(self, board):
		self.board = board
		self.window = pyglet.window.Window()
		self.window.set_handler('on_draw', self.onDraw)
		glClearColor(1, 1, 1, 1)

	def onDraw(self):
		self.window.clear()

	def run(self):
		pyglet.app.run()
