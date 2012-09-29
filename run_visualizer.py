#! /usr/bin/env python

from mm18.visualizer.visualizer import Visualizer
from mm18.game.engine import Engine
from mm18.game.units import Unit
from mm18.game import constants

game = Engine()
game.add_player('p1')
game.tower_create('p1', (0, 2))
game.board_get('p1').queueUnit(
	Unit(1, 0, game.get_player('p1')),
	constants.NORTH
)
viz = Visualizer(game)
viz.run()
