#! /usr/bin/env python

from mm18.visualizer.visualizer import Visualizer
from mm18.game.board import Board

path = [(0, 0), (1, 1), (3, 4)]
board = Board([], path)
viz = Visualizer(board)
viz.run()
