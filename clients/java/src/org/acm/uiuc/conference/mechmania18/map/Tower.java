package org.acm.uiuc.conference.mechmania18.map;

public class Tower extends GameMapPiece {
	private int level = 0;
	private int specialty = 0;
	
	public int getLevel() {
		return this.level;
	}
	
	public int getSpecialty() {
		return this.specialty;
	}

	public void setLevel(int level) {
		this.level = level;
	}
	
	public void setSpecialty(int specialty) {
		this.specialty = specialty;
	}

	public Tower (int level) {
		this.level = level;
	} 
}
