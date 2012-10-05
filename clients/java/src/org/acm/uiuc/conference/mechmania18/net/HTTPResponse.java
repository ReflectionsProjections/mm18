package org.acm.uiuc.conference.mechmania18.net;

import org.json.JSONObject;

public class HTTPResponse {
	private int statusCode = 0;
	private JSONObject response = null;
	
	public int getStatusCode() {
		return statusCode;
	}

	public JSONObject getResponse() {
		return response;
	}

	public HTTPResponse(int statusCode, JSONObject jsonObject) {
		this.statusCode = statusCode;
		this.response = jsonObject;
	}
	
}
