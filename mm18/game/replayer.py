import json

from engine import Engine

class Replayer:
	def __init__(self, actions):
		self.actions = actions
		self.game = Engine()

	def next_action(self):
		return next(self.actions, None)

	def setup_game(self):
		settingUp = True
		while settingUp:
			action = self.next_action()
			settingUp = action and self.play_action(action) != 'start'

	def play_tick(self):
		tickPlaying = True
		while tickPlaying:
			action = self.next_action()
			tickPlaying = action and self.play_action(action) != 'advance'

	def play_action(self, action):
		"""Play an action and returns its type."""
		entry = json.loads(action)
		actionType = entry.pop('action')

		if actionType == 'start':
			pass
		elif actionType == 'advance':
			self.game.advance()
		elif actionType == 'tower_create':
			self.game.tower_create(
				owner_id=entry['owner_id'],
				coords=tuple(entry['coords'])
			)
		else:
			getattr(self.game, actionType)(**entry)

		return actionType
