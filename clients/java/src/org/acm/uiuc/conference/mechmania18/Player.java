package org.acm.uiuc.conference.mechmania18;

import org.acm.uiuc.conference.mechmania18.map.GameMap;

public class Player {
	private int health = -1;
	private int resources = -1;
	private int level = -1;
	private GameMap map = new GameMap();
	
	public int getHealth() {
		return health;
	}

	public void setHealth(int health) {
		this.health = health;
	}

	public int getResources() {
		return resources;
	}

	public void setResources(int resources) {
		this.resources = resources;
	}

	public int getLevel() {
		return level;
	}

	public void setLevel(int level) {
		this.level = level;
	}
	
	public Player(int health, int resources, int level) {
		
	}

	public GameMap getMap() {
		return map;
	}

	public void setMap(GameMap map) {
		this.map = map;
	}
}
