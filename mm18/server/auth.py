import random

class MMAuthenticator():
	"""Mechmania Authenticator System

	Contains authentication data and controls for the server
	"""

	# Constant value for the bits in the token
	_token_size = 32

	def __init__(self, max_clients=4):
		"""Set up an MMAuthenticator

		max_clients - The maximum number of clients that can join the server
		"""

		self._client_tokens = {}
		self._max_clients = max_clients
		random.seed()

	def add_client(self, client_id):
		"""Add a new client to the authenticator

		client_id - The id key for the client's auth lookup
		"""

		if len(self._client_tokens) < self._max_clients \
				and client_id not in self._client_tokens:
			token = self._generate_token()
			self._client_tokens[client_id] = token
			return token
		else:
			return None

	def authorize_client(self, client_id, token):
		"""Check that a given client is authorized.

		client_id - The id key the client was added with
		token - The auth token to check against
		"""

		return client_id in self._client_tokens \
				and self._client_tokens[client_id] == token

	def _generate_token(self):
		"""Generate an auth token for a client to use"""

		return str(random.getrandbits(self._token_size))
