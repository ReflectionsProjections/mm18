package org.acm.uiuc.conference.mechmania18.map;

public abstract class GameMapPiece {
	
	private int pieceId;
	
	protected boolean isTraversible() {
		return false;  // By default, units should not be able to traverse the square.
		               // We don't want units attempting to plan paths through the towers
	}

	public int getPieceId() {
		return pieceId;
	}

	public void setPieceId(int pieceId) {
		this.pieceId = pieceId;
	}
	
}
