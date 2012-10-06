#! /usr/bin/env python

import sys
import argparse

from mm18.visualizer.visualizer import Visualizer

def main():
	parser = argparse.ArgumentParser(
		description='Visualizes MechMania 18 games.')
	parser.add_argument('LOG', type=argparse.FileType('r'),
		help='Log file to replay game from')
	parser.add_argument('PLAYER', nargs='?', default=None,
		help='Player whose Board should be shown')
	args = parser.parse_args()

	lines = args.LOG.readlines()
	args.LOG.close()
	viz = Visualizer(iter(lines), args.PLAYER)
	viz.run()

if __name__ == "__main__":
	sys.exit(main())
