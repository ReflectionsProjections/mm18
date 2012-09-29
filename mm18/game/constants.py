#! /usr/bin/env python

"""Timing Constants"""
# Time each tick takes, in seconds
TICK_TIME = .001
# Maximum amount of ticks for the game to run for
# Currently set to 10 minutes
MAX_RUNTIME = 10 * 60 * 1000

"""TOWERS"""
BASE_TOWER_DAMAGE = 1
# Maximum upgrade level for towers and units
MAX_UPGRADE = 3
TOWER_SELL_SCALAR = 1
TOWER_BASE_COST = 1
TOWER_RANGE = {0:1, 1:1, 2:2}
TOWER_UPGRADE_MULTIPLIER = {0:1, 1:1.5, 2:2.5, 3:3.5}
TOWER_UPGRADE_COST = {1:1, 2:2, 3:3}
TOWER_SPECIALIZE_COST = {1:1, 2:2, 3:3}

"""UNITS"""
UNIT_BASE_COST = 1
BASE_UNIT_HEALTH = 1
BASE_UNIT_DAMAGE = 1
UNIT_UPGRADE_MULTIPLIER = {0:1, 1:1.5, 2:2.5, 3:3.5}
UNIT_UPGRADE_COST = {1:1, 2:2, 3:3}

"""tower/unit specialisation output damage multiplier"""
SUPER_EFFECTIVE = 1.25
EFFECTIVE = 1.1
NORMAL = 1
NOT_EFFECTIVE = 0.75

# specialisation_table[attack][defense]
SPECIALISATION_TABLE = \
  [[NOT_EFFECTIVE,   EFFECTIVE, SUPER_EFFECTIVE],
   [NORMAL,          NORMAL,    NORMAL],
   [SUPER_EFFECTIVE, EFFECTIVE, NOT_EFFECTIVE]]
def specialisation_mulitplier(attack, defense):
	return SPECIALISATION_TABLE[attack+1][defense+1]

"""PLAYER"""
BASE_RESOURCES = 15
UPGRADE_INCREASE = 10
BASE_HEALTH = 1
HEALTH_DECREASE = 1

"""BOARD"""
#Must always be odd
BOARD_SIDE = 11
BASE_SIZE = 3
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

"""MODEL"""
SUPPLY_TIME = 4;
