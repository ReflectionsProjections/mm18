#! /usr/bin/env python

from mm18.visualizer.visualizer import Visualizer

with open('mm18/mocks/game_log.json') as f:
	lines = f.readlines()
viz = Visualizer(iter(lines))
viz.run()
