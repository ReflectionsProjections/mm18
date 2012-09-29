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
	private int port = 80;
	
	public String getHostname() {
		return hostname;
	}

	public void setHostname(String hostname) {
		this.hostname = hostname;
	}

	public int getPort() {
		return port;
	}

	public void setPort(int port) {
		this.port = port;
	}
	
	public MechManiaGameEnvironment(String hostname, int port) {
		this.hostname = hostname;
		this.port = port;
	}
	
}
