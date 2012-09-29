package org.acm.uiuc.conference.mechmania18.map;


public class GameMap {
	private static final int MAP_SIZE = 16;
	
	// For now, we'll assume that 
	private GameMapPiece[][] map = new GameMapPiece[MAP_SIZE][MAP_SIZE];
	
	public GameMap() {
		for (int i = 0; i < MAP_SIZE; i++) {
			for (int j = 0; j < MAP_SIZE; j++) {
				map[i][j] = new AvailableLand();
			}
		}
	}
	
	public boolean canBuildOn(int x, int y) {
		return (map[x][y].getClass() == AvailableLand.class);
	}
	
	public void setSquare(int x, int y, GameMapPiece square) {
		if (x < 0 || x > MAP_SIZE || y < 0 || y > MAP_SIZE) {
			return;
		}
		
		map[x][y] = square;
	}
	
	public GameMapPiece getSquare(int x, int y) {
		return map[x][y];
	}
	
	public int countTowers() {
		int towerCount = 0;
		
		for (int i = 0; i < MAP_SIZE; i++) {
			for (int j = 0; j < MAP_SIZE; j++) {
				GameMapPiece piece = map[i][j];
				
				if (piece.getClass() == Tower.class) {
					towerCount++;
				}
			}
		}
		
		return towerCount;
	}
	
	public final int getMapSize() {
		return MAP_SIZE;
	}
}
