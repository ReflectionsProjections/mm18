package org.acm.uiuc.conference.mechmania18.tests;

import junit.framework.Assert;

import org.acm.uiuc.conference.mechmania18.map.GameMap;
import org.acm.uiuc.conference.mechmania18.map.GameMapPiece;
import org.acm.uiuc.conference.mechmania18.map.Tower;
import org.acm.uiuc.conference.mechmania18.map.TraversiblePath;
import org.junit.Before;
import org.junit.Test;

public class MapTests {

	GameMap map = null;
	Tower tower = null;
	TraversiblePath tpath = null;
	
	@Before
	public void initialize() {
		map = new GameMap();
		tower = new Tower(1);
		tpath = new TraversiblePath();
	}
	
	@Test
	public void testSetSquare() {
		map.setSquare(0, 0, tower);
		
		GameMapPiece returnedPiece = map.getSquare(0, 0);
		Assert.assertEquals(tower.getClass(), returnedPiece.getClass());
	}
	
	@Test
	public void testCanBuildOnTraversiblePath() {
		Assert.assertTrue(map.canBuildOn(0, 0));
		
		map.setSquare(0, 0, tpath);
		Assert.assertFalse(map.canBuildOn(0, 0));
	}
	
	@Test
	public void testCanBuildOnMapObjects() {
		Assert.assertTrue(map.canBuildOn(0, 0));
		
		map.setSquare(0, 0, tower);
		Assert.assertFalse(map.canBuildOn(0, 0));
		
		map.setSquare(0, 0, tpath);
		Assert.assertFalse(map.canBuildOn(0, 0));
	}
	
	@Test
	public void testTowerCounter() {
		int size = map.getMapSize();
		
		Assert.assertEquals(0, map.countTowers());
		
		map.setSquare(0, 0, tower);
		Assert.assertEquals(1, map.countTowers());
		
		for(int i = 0; i < size; i++) {
			for(int j = 0; j < size; j++) {
				map.setSquare(i, j, tower);
			}
		}
		
		Assert.assertEquals(size*size, map.countTowers());
	}
}
