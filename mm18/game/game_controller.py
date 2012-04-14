#!/usr/bin/env python

class GameController(object):
	"""
	Basic class for facilitating communication between the server, game
	database, and logic/rules of the game.

	Static class. Should not need initialization.
	"""

	@staticmethod
	def init_game(self, game_info):
		"""
		Create a new running game and get its ID.

		game_info - Dictionary of game setup data
		"""

	@staticmethod
	def send_to_game(self, message, game):
		"""
		Process a message and send it to the active game

		message - The message to send to the game
		game - Game ID to send to
		"""

		pass

	@staticmethod
	def get_from_game(self, message, game):
		"""
		Process a message and send it to the active game

		message - The message describing what to recover
		game - Game ID to send to
		"""

		pass

	@staticmethod
	def get_game_info(self, game):
		"""
		Recover a predefined dictionary of game data.

		game - Game ID to get information from
		"""

		pass

	@staticmethod
	def get_object(self, **args):
		"""
		Returns a representation of the specified object
		"""

		if args['obj'] == 'towers':
			return 1
		else:
			return -1

	@staticmethod
	def upgrade_object(self, **args):
		"""
		Upgrade the specified object (i.e. upgrade a tower)

		Returns a representation of the upgraded version of the object
		"""

		if get_object(self, **args) == 1:
			return args['id']
		else:
			return -1
