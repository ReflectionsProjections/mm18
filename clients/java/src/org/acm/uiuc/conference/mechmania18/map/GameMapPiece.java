package org.acm.uiuc.conference.mechmania18.map;

public abstract class GameMapPiece {
	
	protected boolean isTraversible() {
		return false;  // By default, units should not be able to traverse the square.
		               // We don't want units attempting to plan paths through the towers
	}
	
}
