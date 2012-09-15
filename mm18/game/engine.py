class Engine():

	def __init__(self):
		pass

	# Game controls

	def advance(self):
		pass

	# Player controls

	def get_player_ids(self):
		pass

	def get_player(self, player_id):
		pass

	# Board Class Controls

	def get_board(self, player_id):
		pass

	# Tower Class Controls

	def tower_create(self, owner_id, coords, level, spec):
		pass

	def tower_upgrade(self, tower_id, owner_id):
		pass

	def tower_sell(self, tower_id, owner_id):
		pass

	def tower_specialize(self, tower_id, owner_id, spec):
		pass

	# Unit Class Controls

	def unit_create(self, owner_id, level, spec, target_id, path):
		pass
