import os
import pyglet
from pyglet.gl import *

from mm18.game import constants
from mm18.game.board import Board
from mm18.game.replayer import Replayer

TILE_SIZE = 32
PADDING = TILE_SIZE
TICKS_PER_SECOND = 10
BOARD_ROWS = 2
BOARD_COLS = 2

resources_path = os.path.join(os.path.dirname(__file__), 'resources')
pyglet.resource.path.append(resources_path)
pyglet.resource.reindex()

tex_terrain = pyglet.resource.image('grass.png')
tex_path = pyglet.resource.image('path.png')
tex_base = pyglet.resource.image('base.png')
tex_base_mid = pyglet.resource.image('base_mid.png')
tex_base_low = pyglet.resource.image('base_low.png')
tex_tower = pyglet.resource.image('tower.png')
tex_unit = pyglet.resource.image('unit.png')
tex_explosion = pyglet.resource.image('explosion.png')

class Visualizer:

	def __init__(self, actions, player_ids=None):
		self.replayer = Replayer(actions)
		self.replayer.setup_game()
		self.game = self.replayer.game
		if player_ids:
			self.player_ids = player_ids
		else:
			self.player_ids = self.game.get_player_ids()
		self.tick_summary = None

		cols = BOARD_COLS if len(self.player_ids) > 1 else 1
		rows = BOARD_ROWS if len(self.player_ids) > 2 else 1
		self.window = pyglet.window.Window(
			width=cols * TILE_SIZE * constants.BOARD_SIDE + (cols - 1) * PADDING,
			height=rows * (TILE_SIZE * constants.BOARD_SIDE + PADDING),
		)
		self.window.set_handler('on_draw', self.draw)
		pyglet.clock.schedule_interval(self.update, 1.0 / TICKS_PER_SECOND)
		glClearColor(1, 1, 1, 1)
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

	def update(self, dt=0):
		# parse and perform commands from log
		# advance the game controller
		self.tick_summary = self.replayer.play_tick()
		if self.tick_summary == None:
			pyglet.clock.unschedule(self.update)

	def draw(self):
		self.window.clear()

		width = TILE_SIZE * constants.BOARD_SIDE + PADDING
		height = TILE_SIZE * constants.BOARD_SIDE + PADDING
		pos = 0
		for player_id in self.player_ids:
			player = self.game.get_player(player_id)
			if not player.isDead():
				glMatrixMode(GL_MODELVIEW)
				glLoadIdentity()
				x = pos % BOARD_COLS
				y = pos / BOARD_COLS
				glTranslatef(width * x, height * y, 0)
				self.drawPlayer(player)
				self.drawLabel(player)
			pos += 1

	def drawPlayer(self, player):
		# Draw features of the Board
		board = player.board
		tiles = ((x, y) for x in range(board.width) for y in range(board.height))
		for (x, y) in tiles:
			tex = tex_path if (x, y) in board.path else tex_terrain
			tex.blit(
				x=TILE_SIZE * x,
				y=TILE_SIZE * y,
				width=TILE_SIZE,
				height=TILE_SIZE,
			)
		self.drawBases(board.base, player.health)
		self.drawTowers(board.tower)
		for path in board.paths.itervalues():
			self.drawUnits(path)

		# Draw effects from the summary
		player_summary = None
		if self.tick_summary:
			player_summary = self.tick_summary.get(player.name)
		if player_summary and player_summary.get('deaths'):
			for death in player_summary['deaths']:
				self.drawDeadUnit(death['unit'], death['unit_pos'])
		if player_summary and player_summary.get('attacks'):
			for attack in player_summary['attacks']:
				self.drawAttack(attack)

	def drawBases(self, bases, health):
		for coords in bases:
			self.drawBase(coords, health)

	def drawBase(self, coords, health):
		(x, y) = coords
		if health <= 33:
			tex = tex_base_low
		elif health <= 66:
			tex = tex_base_mid
		else:
			tex = tex_base
		tex.blit(
			x=TILE_SIZE * x,
			y=TILE_SIZE * y,
			width=TILE_SIZE,
			height=TILE_SIZE,
		)

	def drawTowers(self, towers):
		for coords in towers.iterkeys():
			self.drawTower(towers[coords], coords)

	def drawTower(self, tower, coords):
		(x, y) = coords
		tex_tower.blit(
			x=TILE_SIZE * x,
			y=TILE_SIZE * y,
			width=TILE_SIZE,
			height=TILE_SIZE,
		)

	def drawUnits(self, path):
		for unit, coords in path.entries():
			if unit and unit.health > 0:
				self.drawUnit(unit, coords)

	def drawUnit(self, unit, coords):
		(x, y) = coords
		tex_unit.blit(
			x=TILE_SIZE * x,
			y=TILE_SIZE * y,
			width=TILE_SIZE,
			height=TILE_SIZE,
		)

	def drawDeadUnit(self, unit, coords):
		(x, y) = coords
		tex_explosion.blit(
			x=TILE_SIZE * x,
			y=TILE_SIZE * y,
			width=TILE_SIZE,
			height=TILE_SIZE,
		)

	def drawAttack(self, attack):
		(xt, yt) = attack['tower_pos']
		(xu, yu) = attack['unit_pos']
		glColor3f(1, 0, 0)
		pyglet.graphics.draw(2, GL_LINES, ('v2f', (
			TILE_SIZE * (xt + .5), TILE_SIZE * (yt + .5),
			TILE_SIZE * (xu + .5), TILE_SIZE * (yu + .5)
		)))
		# If we don't set the color back to white, the screen turns red
		glColor3f(1, 1, 1)

	def drawLabel(self, player):
		text = 'Team: %s, Level: %d, Health: %.2f, Resources: %d' % (
			player.name,
			player.allowedUpgrade,
			player.health,
			player.resources
		)
		margin = 6
		label = pyglet.text.Label(
			text=text,
			color=(0, 0, 0, 255),
			x=margin,
			y=TILE_SIZE * constants.BOARD_SIDE + margin,
			width=TILE_SIZE * constants.BOARD_SIDE - margin,
			height=PADDING,
		)
		label.draw()

	def run(self):
		pyglet.app.run()
