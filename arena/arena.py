#! /usr/bin/env python

# The arena is responsible for pitting teams against each other
# It expects to run from a folder containing the clients for it to run

import sys
import time
import threading
import subprocess
import os
import os.path

from mm18.server import server

# Component functions
def update_teams(teams):
	names = {}
	name_set = set()
	for team in teams:
		# Pull in teams and bring them to the arena
		# TODO: Pull from bitbucket
		# Update their name
		try:
			group_name = read_name(team)
		except IOError:
			group_name = str(team)

		if group_name in name_set:
			# Team already exists
			print "WARN: Team has same name as other team"
			if str(team) in name_set:
				print "ERROR: Team is not unique. Kill it with fire"
				sys.exit(1)
			print "Defaulting on unique string", str(team)
			group_name = str(team)

		name_set.add(group_name)
		names[team] = group_name
		print "Team " + str(team) + ": " + group_name
		print "Welcome to the arena!"
	for team in teams:
		# Run their makescript
		path = "./" + team + "/Makescript"
		print "Building client for team", team
		try:
			subprocess.call([path])
		except OSError:
			print "WARN: Build failed on team", team

	return names

def read_name(team):
	path = str(team) + "/GROUP"
	groups_file = open(path)
	return groups_file.readline().strip()

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
		# We tell the server the name to give the player
		server.global_client_manager.set_next_team(int(team))
		outpath = team + "/out.txt"
		outfile = open(outpath, "w+")
		errpath = team + "/err.txt"
		errfile = open(errpath, "w+")
		team_cwd = os.getcwd() + '/' + str(team)
		subprocess.Popen([path, address], stdout=outfile, stderr=errfile, cwd=team_cwd)
		# Wait for the server to connect before continuing
		cycles = 0
		while True:
			if server.global_client_manager.get_set_status():
				break
			if cycles >= 5:
				print "ERROR: Team", team, "timed out on connect"
				sys.exit(1)
			cycles += 1
			time.sleep(1)

# Competition control functions
def run_competition():
	pass

def main(server_addr, server_port, game_log, teams):
	# First, pull in the latest code for the teams to run
	names = update_teams(teams)

	# Second, start the server on the given port
	full_addr = server_addr + ":" + str(server_port)
	print "Arena is starting the server on", full_addr
	start_server(server_addr, server_port, game_log)

	for name in names:
		print "Team " + names[name] + " playing as " + name

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
