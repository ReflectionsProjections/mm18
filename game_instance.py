from old_code.game_map import Map
from old_code.game import Game

game_time = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
log_file = 'logs/game-%s' % game_time
inited = False
# These values should be inited somewhere else
# XXX: Old test cases rely on them being inited here
game_map = Map(2)
game = Game(game_map, log_file)
