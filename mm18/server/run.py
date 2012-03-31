#!/usr/bin/env python

import server

def Main():
	serve = server.ThreadedHTTPServer(('localhost', 6969), server.MMHandler)
	# This prevents errors where the socket is still bound
	serve.allow_reuse_address = True
	# TODO: Make the server have an option to exit gracefully
	print "Server starting on port 6969"
	serve.serve_forever()

if __name__ == '__main__':
	Main()
