"""URL Patterns for mapping URLs to the appropriate functions."""

from mm18.game.game_controller import *

urlpatterns = [
	# Commands for overall game
	(r'/game/status', 'POST', get_game_status),

	# Commands for player control, status, etc
	(r'/player/(?P<id>\d+)', 'POST', get_player_status),

	# Commands for retrieving representation details
	(r'/board/(?P<id>\d+)', 'POST', board_get),

	# Tower API
	(r'/tower/(?P<id>\d+)/upgrade', 'POST', tower_upgrade),
	(r'/tower/(?P<id>\d+)/specialize', 'POST', tower_specialize),
	(r'/tower/(?P<id>\d+)/sell', 'POST', tower_sell),
	(r'/tower/(?P<id>\d+)', 'POST', tower_get),
	(r'/tower/create', 'POST', tower_create),

	# Unit API
	(r'/unit/create', 'POST', unit_create),

	# Constants API
	(r'/constants', 'POST', constants_get),

	# Connection API
	# This exists, but is implemented in server. Leave it here to document.
	# I'm aware it's not the prettiest of solutions.
	#(r'/connect', 'POST', connect),
]
