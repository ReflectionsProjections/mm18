package org.acm.uiuc.conference.mechmania18;

import org.acm.uiuc.conference.mechmania18.net.HTTPResponse;
import org.acm.uiuc.conference.mechmania18.net.MechManiaHTTP;
import org.json.JSONException;
import org.json.JSONObject;

public class MechMania {
	private String gameKey;
	private int myteam;

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
		
		// Join server
		if (!joinServer(http)) {
			System.out.println("Failed to join server");
			return;
		}
		
		// Main loop - core game logic should go here or be called from here
		boolean stillPlaying = true;
		while (stillPlaying) {
			updateStatus(http);
			attack(http, (int)Math.floor(Math.random() * 4)+1);
		}
		
		return;
	}
	
	/**
	 * Requests game status information from 
	 * 
	 * @param http
	 */
	private void updateStatus(MechManiaHTTP http) {
		HTTPResponse response = null;
		
		try {
			response = http.makeRequest("/game/status", new JSONObject("{\"id\":" + myteam + "," + 
					"\"auth\":\"" + gameKey + "\"}"));
		} catch (JSONException e) {
			e.printStackTrace();
		}
		
		
		
		// Handle updating map information, player information, etc.
		
		return;
	}

	/**
	 * Attempts to send a join message to the game server 
	 * 
	 * @param http The MechManiaHTTP object initialized with game server settings
	 * @return True on successful join attempt
	 */
	private boolean joinServer(MechManiaHTTP http) {
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
	 * Attempts to send an attack command to the game server (and units to an enemy, etc. etc.)
	 * 
	 * @param http The MechManiaHTTP object initialized with game server settings
	 * @param target The integer ID of the player being targeted
	 * @return True on successful unit deployment
	 */
	private boolean attack(MechManiaHTTP http, int target) {
		if (target < 1 || target > 4 || target == myteam) {
			return false;
		}
		
		HTTPResponse response = null;
		try {
			response = http.makeRequest("/unit/create", new JSONObject("{\"id\":" + myteam + "," + 
					"\"auth\":\"" + gameKey + "\"," + "\"path\":0," +
					"\"level\":1," + "\"target_id\":" + myteam + ",\"spec\":0}"));
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
	
}
