#! /usr/bin/env python

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
    def __init__ (self, positionX, positionY)
        self.positionX = positionX
        self.positionY = positionY
        self.upgrade = 0
        self.upgradeCost = 1
        self.specialisation = 0

    """
    Upgrades the tower.
    This is assuming that checking whether an upgrade is allowed is done elsewhere.
    """
   # def upgrade(self)
        
