#!/usr/bin/env python

import server

def Main():
	
	import logging
	# Starts logging function
	logging.basicConfig(filename='Server.log',level=logging.DEBUG)
	logging.debug('Logging function started')
	# Sets logging level - available options are DEBUG, INFO, WARNING, ERROR, CRITICAL
	
	serve = server.ThreadedHTTPServer(('localhost', 6969), server.MMHandler)
	# This prevents errors where the socket is still bound
	serve.allow_reuse_address = True
	# TODO: Make the server have an option to exit gracefully
	print "Server starting on port 6969"
	serve.serve_forever()

if __name__ == '__main__':
	Main()
