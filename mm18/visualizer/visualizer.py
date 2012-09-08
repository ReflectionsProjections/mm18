#! /usr/bin/env python

import pyglet
from pyglet.gl import *

class Visualizer:
	def __init__(self):
		self.window = pyglet.window.Window()
		self.window.set_handler('on_draw', self.onDraw)
		glClearColor(1, 1, 1, 1)

	def onDraw(self):
		self.window.clear()

	def run(self):
		pyglet.app.run()

if __name__ == '__main__':
	viz = Visualizer()
	viz.run()
