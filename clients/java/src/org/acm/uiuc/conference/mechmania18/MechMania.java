package org.acm.uiuc.conference.mechmania18;

import org.acm.uiuc.conference.mechmania18.map.GameMap;
import org.acm.uiuc.conference.mechmania18.map.GameMapPiece;
import org.acm.uiuc.conference.mechmania18.map.Tower;
import org.acm.uiuc.conference.mechmania18.net.HTTPResponse;
import org.acm.uiuc.conference.mechmania18.net.MechManiaHTTP;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class MechMania {
	private String gameKey;
	private int myteam;
	private Player[] players;

	/**
	 * MechMania dispatch
	 * 
	 * Most of the logic for the game will be contained by or called here.  This is where the magic happens.
	 * 
	 * @param environment MechManiaGameEnvironment object with connection information for a match
	 */
	public void start (MechManiaGameEnvironment environment) {
		// Inititalize HTTP component
		MechManiaHTTP http = new MechManiaHTTP(environment.getHostname());
		
		// Initialize the players array
		players = new Player[4];
		for (int i = 0; i < 4; i++) {
			players[i] = new Player(-1,-1,-1);
		}
		
		// Join server
		try {
			if (!joinServer(http)) {
				System.out.println("Failed to join server");
				return;
			}
		} catch (GameOverException e1) {
			return;
		}
		
		// Main loop - core game logic should go here or be called from here
		boolean stillPlaying = true;
		while (stillPlaying) {
			try {
				//updateStatus(http);  // Redundant per updatePlayer
				for (int i = 0; i < 4; i++) {
					updatePlayer(http, i);
					getBoard(http, i);
				}
				attack(http, (int)Math.floor(Math.random() * 4)+1, (int)Math.floor(Math.random() * 4), 1, 0);
				buildTower(http, (int)Math.floor(Math.random() * 16), (int)Math.floor(Math.random() * 16), 0, 0);
			}
			catch (GameOverException e) {
				return;
			}
		}
		
		return;
	}
	
	/**
	 * Requests game status information from the server...
	 * 
	 * @param http
	 */
	private void updateStatus(MechManiaHTTP http) throws GameOverException {
		HTTPResponse response = null;
		
		try {
			JSONObject reqObj = buildBaseJSONObject();
			
			response = http.makeRequest("/game/status", reqObj);
			
			JSONArray playerJson = response.getResponse().getJSONArray("players");
			
			for (int i = 0; i < 4; i++) {
				JSONArray healthJson = playerJson.getJSONArray(i);
				
				players[healthJson.getInt(0)].setHealth(healthJson.getInt(1));
			}
			
			
		} catch (JSONException e) {
			return;
		} catch (GameOverException e) {
			e.printStackTrace();
		}
		
		return;
	}

	/**
	 * Builds a basic JSONObject with the authentication tokens we need to pass
	 * 
	 * @return JSONObject with authentication tokens pre-added
	 * @throws JSONException
	 */
	private JSONObject buildBaseJSONObject() throws JSONException {
		JSONObject baseObject = new JSONObject();
		
		baseObject.put("id", myteam);
		baseObject.put("auth", gameKey);
		
		return baseObject;
	}

	/**
	 * Requests the status of a particular player
	 *
	 * @param http The configured MechMania HTTP object
	 * @param playerId The player ID to look up 
	 */
	private void updatePlayer(MechManiaHTTP http, int playerId) throws GameOverException {
		HTTPResponse response = null;
		
		try {
			JSONObject reqObj = buildBaseJSONObject();
			
			response = http.makeRequest("/player/" + playerId, reqObj);
			
			JSONObject data = response.getResponse();
			players[playerId].setHealth(data.getInt("health"));
			
			if (playerId == myteam) {
				// We likely got some extra information in our results, so let's use it
				players[playerId].setResources(data.getInt("resources"));
				players[playerId].setLevel(data.getInt("level"));
			}
		} catch (JSONException e) {
			e.printStackTrace();
		} catch (GameOverException e) {
			e.printStackTrace();
		}
		
		// Update the recorded information about the player (health, etc.)
		
		return;
	}


	/**
	 * Attempts to send a join message to the game server 
	 * 
	 * @param http The MechManiaHTTP object initialized with game server settings
	 * @return True on successful join attempt
	 */
	private boolean joinServer(MechManiaHTTP http) throws GameOverException {
		System.out.println("Making join request, this may take a while!");
		HTTPResponse response = http.makeRequest("/connect");
		
		if (response.getStatusCode() == 200) {
			JSONObject joinResponse = response.getResponse();
			try {
				this.gameKey = joinResponse.getString("auth");
				this.myteam = joinResponse.getInt("id");
			} catch (JSONException e) {
				e.printStackTrace();
			}
		}
		
		return (response.getStatusCode() == 200);
	}

	/**
	 * Attempts to build a new tower in a specified location
	 * 
	 * @param http The MechManiaHTTP object initialized with game server settings
	 * @param x The grid x coordinate of the desired tower
	 * @param y The grid y coordinate of the desired tower
	 * @param level The desired level of tower to construct
	 * @param specialization The desired specialization class of the tower
	 * @return True on successful tower build
	 */
	private boolean buildTower(MechManiaHTTP http, int towerx, int towery, int level, int specialization) throws GameOverException {
		if (towerx < 0 || towerx > 15 || towery < 0 || towery > 15 || Math.abs(specialization) > 1) {
			return false;
		}

		HTTPResponse response = null;
		try {
			JSONObject reqObj = buildBaseJSONObject();
			
			reqObj.put("position", new int[]{towerx, towery});
			reqObj.put("level", level);
			reqObj.put("spec", specialization);
					
			response = http.makeRequest("/tower/create", reqObj);
		} catch (JSONException e) {
			e.printStackTrace();
		}
		switch (response.getStatusCode()) {
		case 200:
			// Handle updating map with new tower
			return true;
		case -1:
		default:
			return false;
		}

	}

	
	/**
	 * Attempts to send an attack command to the game server (and units to an enemy, etc. etc.)
	 * 
	 * @param http The MechManiaHTTP object initialized with game server settings
	 * @param target The integer ID of the player being targeted
	 * @param path The path to use
	 * @param level The level of unit to send
	 * @param specialization The specialization of the unit to send
	 * @return True on successful unit deployment
	 */
	private boolean attack(MechManiaHTTP http, int target, int path, int level, int specialization) throws GameOverException {
		if (target < 1 || target > 4 || target == myteam || Math.abs(specialization) > 1) {
			return false;
		}
		
		HTTPResponse response = null;
		try {
			JSONObject reqObj = buildBaseJSONObject();
			reqObj.put("path", path);
			reqObj.put("target_id", target);
			reqObj.put("level", level);
			reqObj.put("spec", specialization);
			
			response = http.makeRequest("/unit/create", reqObj);
		} catch (JSONException e) {
			e.printStackTrace();
		}
		switch (response.getStatusCode()) {
		case 200:
			return true;
		case -1: // Add additional codes to update logic
		default:
			return false;
		}
	}
	
	/**
	 * Get the details of a specified player's game board
	 * 
	 * @param http The MechManiaHTTP object initialized with game server settings
	 * @param playerId The player ID to look up 
	 * @return True on successful request
	 * @throws GameOverException
	 */
	private boolean getBoard(MechManiaHTTP http, int playerId) throws GameOverException {
		
		HTTPResponse response = null;
		try {
			JSONObject reqObj = buildBaseJSONObject();
			
			response = http.makeRequest("/board/" + playerId,reqObj);
			
			JSONObject board = response.getResponse();
			
			JSONArray towers = board.getJSONArray("towers");
			JSONArray path = board.getJSONArray("paths");
			JSONArray units = board.getJSONArray("units");
			
			// Meh.
			
		} catch (JSONException e) {
			e.printStackTrace();
		}
		
		return false;
	}

}
