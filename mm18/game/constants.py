#! /usr/bin/env python

#import json

"""TOWERS & UNITS"""
BASE_DAMAGE = 1 #this is currently for both towers and units.  May need to create separate ones for towers and units.
MAX_UPGRADE = 3 #max upgrade level for towers and units
BASE_UNIT_HEALTH = 1

"""Costs"""
TOWER_BASE_COST = 1
UNIT_BASE_COST = 1
TOWER_UPGRADE_ONE_COST = 1

"""
Dictionaries for upgrades/multipliers
"""
UPGRADE_MULTIPLIER = {0:1, 1:1.5, 2:2.5, 3:3.5}
UPGRADE_COST = {1:1.5, 2:2.5, 3:3.5}

"""tower/unit specialisation output damage multiplier"""
SUPER_EFFECTIVE = 1.25
EFFECTIVE = 1.1
NORMAL = 1
NOT_EFFECTIVE = 0.75

"""PLAYER"""
BASE_RESOURCES = 15
UPGRADE_INCREASE = 10

"""BOARD"""
BASE_HEALTH = 1
BOARD_SIDE = 5

"""PLACEHOLDER"""
BOOP = -1000
