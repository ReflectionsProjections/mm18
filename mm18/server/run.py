#!/usr/bin/env python

import server
import logging
import sys

def Main(**kwargs):
	"""Run the MechMania server

	Contains settings for the server logging function. Starts server logging
	function. Starts server on port 6969 and serves forever.
	"""
	
	if 'game_log' in kwargs:
		server.game_log = kwargs['game_log']
	serve = server.ThreadedHTTPServer(('localhost', 6969), server.MMHandler)
	# This prevents errors where the socket is still bound
	serve.allow_reuse_address = True
	print "Server starting on port 6969"
	serve.serve_forever()

if __name__ == '__main__':
	if len(sys.argv) > 1:
		Main(game_log=sys.argv[1])
	else:
		Main()
