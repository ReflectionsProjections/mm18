#!/usr/bin/env python

import server
import logging

def Main(**kwargs):
	"""Run the MechMania server

	Contains settings for the server logging function. Starts server logging
	function. Starts server on port 6969 and serves forever.
	"""

	# Starts logging function
	logging.basicConfig(format=kwargs['log_format'],
			filename=kwargs['log_file'])
	log = logging.getLogger()
	log.setLevel(kwargs['log_level'])
	logging.info('Logging function started')

	serve = server.ThreadedHTTPServer(('localhost', 6969), server.MMHandler)
	# This prevents errors where the socket is still bound
	serve.allow_reuse_address = True
	# TODO: Make the server have an option to exit gracefully
	print "Server starting on port 6969"
	logging.info('Server starting on port 6969')
	serve.serve_forever()

if __name__ == '__main__':
	# LOG SETTINGS
	# log_file - the filename to output logging to. Saved to the same directory as this file.
	# log_format - format to write log messages in
	# log_level - threshold for logging. Options are logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
	
	log_file_name = 'Server.log'
	log_format_str = '%(levelname)s: %(message)s'
	log_level_flag = logging.INFO

	Main(log_file=log_file_name, log_format=log_format_str, log_level=log_level_flag)
