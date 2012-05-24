#! /usr/bin/env python

import constants

"""
This is the tower class
Towers get created here.
I'm thinking have this as a superclass and make the specialised classes from this?
Or not - it may just be easier to put it all in here because towers don't need a lot
All towers need:
    -A position
    -A specialisation (or lack)
    -Tower upgrade level

Class contents:
    -init
    -upgrad
"""

class Tower:

    """
    Creates a new Tower at grid positions X and Y.
    All towers start with 0 upgrades and no specialisation.

    @param positionX: The X position of the tower
    @param positionY: The Y position of the tower
    """
    def __init__ (self, positionX, positionY):
        self.positionX = positionX
        self.positionY = positionY
        self.upgrade = 0
        self.specialisation = 0

    """
    Upgrades the tower.
    This will also check to ensure the upgrade can be made once that is implemented
    Currently using 0 because I have no variable for player resources.
    """
    def upgrade(self):
        PLAYER_RESOURCES = 10
        if self.upgrade == 3:
            print "Fully upgraded"
        elif PLAYER_RESOURCES >= constants.UPGRADE_COST[self.upgrade + 1]:
            self.upgrade += 1
            PLAYER_RESOURCES -= constants.UPGRADE_COST[self.upgrade]
            print "Tower level is now:", self.upgrade, "\nPlayer resources are now:", PLAYER_RESOURCES
        else:
            print "Sommat fucked up"


