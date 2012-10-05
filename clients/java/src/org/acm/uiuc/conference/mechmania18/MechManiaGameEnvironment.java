package org.acm.uiuc.conference.mechmania18;

/**
 * MechMania Game Environment
 * 
 * Serves as an intermediary between the game and the startup handler for incoming parameters
 * 
 * Rather than build an HTTP object directly, this could be expanded to carry other contestant-defined parameters across.
 * 
 * @author Nick
 *
 */

public class MechManiaGameEnvironment {
	private String hostname = "";
	
	public String getHostname() {
		return hostname;
	}

	public void setHostname(String hostname) {
		this.hostname = hostname;
	}

	public MechManiaGameEnvironment(String hostname) {
		this.hostname = hostname;
	}
	
}
