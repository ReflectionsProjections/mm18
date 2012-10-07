from auth import MMAuthenticator

import threading

class MMClientManager():
	"""Mechmania Client Manager

	Contains information about clients, how many can connect, and auth info
	for the clients.
	"""

	def __init__(self, max_clients=4):
		self.clients = []
		self.auth = MMAuthenticator()
		self._max_clients = max_clients
		self._run_lock = threading.Lock()
		self.game_condition = threading.Condition(self._run_lock)
		self._preset_set = False
		self._preset_used = False

	def add_client(self):
		"""Add a new client to the game.

		If the server is full, fails. Otherwise adds a new client to the game,
		returning a tuple with client_id as the first value and auth_token as
		the second. Failure returns None.
		"""
		with self._run_lock:
			if len(self.clients) >= self._max_clients:
				return None
			else:
				if self._preset_set and not self._preset_used:
					client_id = self._preset
					self._preset_used = True
				else:
					# Give the player the next available client id
					# Once connected, a client never loses their place in the server.
					client_id = len(self.clients) + 1

				self.clients.append(client_id)
				auth_token = self.auth.add_client(client_id)
				return (client_id, auth_token)

	def set_next_team(self, name):
		with self._run_lock:
			self._preset_set = True
			self._preset_used = False
			self._preset = name

	def get_set_status(self):
		return self._preset_used

	def is_full(self):
		return len(self.clients) >= self._max_clients
