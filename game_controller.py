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
