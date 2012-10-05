#! /usr/bin/env python

# The arena is responsible for pitting teams against each other
# It expects to run from a folder containing the clients for it to run

import sys
import threading
import subprocess
import os.path

from mm18.server import server

# Component functions
def update_teams(teams):
	pass

def start_server(server_addr, server_port, game_log):
	server.game_log = game_log
	serve = server.ThreadedHTTPServer((server_addr, server_port), server.MMHandler)
	serve.allow_reuse_address = True
	server.server_instance = serve
	thread = threading.Thread(target=serve.serve_forever)
	thread.start()

def run_clients(teams, address):
	for team in teams:
		path = "./" + team + "/client"
		print "Starting client for team", team
		subprocess.Popen([path, address])

# Competition control functions
def run_competition():
	pass

def main(server_addr, server_port, game_log, teams):
	# First, pull in the latest code for the teams to run
	update_teams(teams)

	# Second, start the server on the given port
	full_addr = server_addr + ":" + str(server_port)
	print "Arena is starting the server on", full_addr
	start_server(server_addr, server_port, game_log)

	# Third, run the clients
	run_clients(teams, full_addr)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		game_log = os.path.abspath(sys.argv[1])
	else:
		print "Error, need a game log file"
		sys.exit(1)

	if len(sys.argv) > 5:
		teams = sys.argv[2:6]
	else:
		print "Error, need four team names"
		sys.exit(1)

	main('localhost', 6969, game_log, teams)
