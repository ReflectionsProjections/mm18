#!/usr/bin/env python

import server
import logging

def Main():
	"""Run the MechMania server

	Contains settings for the server logging function. Starts server logging
	function. Starts server on port 6969 and serves forever.
	"""
	
	# LOG SETTINGS
	# log_file - the filename to output logging to. Saved to the same directory as this file.
	# log_format - format to write log messages in
	# log_level - threshold for logging. Options are logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
	
	log_file = 'Server.log'
	log_format = '%(levelname)s: %(message)s'	
	log_level = logging.INFO

	# Starts logging function
	logging.basicConfig(format=log_format,filename=log_file)
	log = logging.getLogger()
	log.setLevel(log_level)
	logging.info('Logging function started')
	

	serve = server.ThreadedHTTPServer(('localhost', 6969), server.MMHandler)
	# This prevents errors where the socket is still bound
	serve.allow_reuse_address = True
	# TODO: Make the server have an option to exit gracefully
	print "Server starting on port 6969"
	logging.info('Server starting on port 6969')
	serve.serve_forever()

if __name__ == '__main__':
	Main()
