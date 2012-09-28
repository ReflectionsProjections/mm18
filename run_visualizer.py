#! /usr/bin/env python

from mm18.visualizer.visualizer import Visualizer
from mm18.game.engine import Engine

game = Engine()
game.add_player('p1')
game.tower_create(
	owner_id='p1',
	coords=(0, 2),
	level=1,
	spec=0
)
viz = Visualizer(game.board_get('p1'))
viz.run()
