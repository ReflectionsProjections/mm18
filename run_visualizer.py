#! /usr/bin/env python

from mm18.visualizer.visualizer import Visualizer
from mm18.game.board import Board

board = Board.jsonLoad('board1.json')
viz = Visualizer(board)
viz.run()
