from auth import MMAuthenticator

class MMClientManager():
	"""Mechmania Client Manager

	Contains information about clients, how many can connect, and auth info
	for the clients.
	"""

	def __init__(self, max_clients=4):
		self.clients = []
		self.auth = MMAuthenticator()
		self._max_clients = max_clients

	def add_client(self):
		"""Add a new client to the game.

		If the server is full, fails. Otherwise adds a new client to the game,
		returning a tuple with client_id as the first value and auth_token as
		the second. Failure returns None.
		"""
		if len(self.clients) >= self._max_clients:
			return None
		else:
			# Give the player the next available client id
			# Once connected, a client never loses their place in the server.
			client_id = len(self.clients) + 1
			self.clients.append(client_id)
			auth_token = self.auth.add_client(client_id)
			return (client_id, auth_token)

	def is_full(self):
		return len(self.clients) >= self._max_clients
