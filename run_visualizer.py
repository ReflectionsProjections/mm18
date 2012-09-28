#! /usr/bin/env python

from mm18.visualizer.visualizer import Visualizer
from mm18.game.engine import Engine

game = Engine()
game.add_player('p1')
game.tower_create('p1', (0, 2))
viz = Visualizer(game)
viz.run()
