"""URL Patterns for mapping URLs to the appropriate functions."""

from mm18.game.game_controller import *

urlpatterns = [
	# Commands for overall game
	(r'/game/status', 'GET', get_game_status),

	# Commands for player control, status, etc
	(r'/player/(?P<id>\d+)', 'GET', get_player_status),

	# Commands for retrieving representation details
	(r'/board/(?P<id>\d+)', 'GET', board_get),

	# Tower API
	(r'/tower/(?P<id>\d+)/upgrade', 'POST', tower_uprade),
	(r'/tower/(?P<id>\d+)/specialize', 'POST', tower_specialize),
	(r'/tower/(?P<id>\d+)/sell', 'POST', tower_sell),
	(r'/tower/(?P<id>\d+)', 'GET', tower_get),
	(r'/tower/create', 'POST', tower_create),
	(r'/tower', 'GET', tower_list),

	# Unit API
	(r'/unit/(?P<id>\d+)', 'GET', unit_status),
	(r'/unit/create', 'POST', unit_create),
]
