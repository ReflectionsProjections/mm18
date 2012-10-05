import json

from engine import Engine

class Replayer:
	def __init__(self, actions):
		self.actions = actions
		self.game = Engine()

	def next_action(self):
		line = next(self.actions, None)
		if line:
			return json.loads(line)
		else:
			return None

	def setup_game(self):
		while True:
			action = self.next_action()
			if not action or action['action'] == 'start':
				break;
			self.play_action(action)

	def play_tick(self):
		while True:
			action = self.next_action()
			if not action:
				return None
			elif action['action'] == 'advance':
				return self.game.advance()
			self.play_action(action)
		return None

	def play_action(self, entry):
		"""Play an action and returns its type."""
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
