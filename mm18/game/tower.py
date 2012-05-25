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

    """
    Specialises the towers provided the towers have not been upgraded and specialisation input is valid.
    Currently using 0 for no specialisation and 1, -1 for the different ones.

    @param spec: either 1, 0 or -1.  Indicates a specialisation.
    """
   def specialise(self,spec):
        if self.upgrade == 0 & spec >= -1 & spec <= 1:
            self.specialisation = spec
            print "New specialisation is:", self.specialisation
        else:
            print "Either spec is not valid or object is already upgraded"

