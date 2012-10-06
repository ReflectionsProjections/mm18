package org.acm.uiuc.conference.mechmania18.net;

import java.io.BufferedInputStream;
import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.SocketException;
import java.net.URL;

import org.acm.uiuc.conference.mechmania18.GameOverException;
import org.json.JSONException;
import org.json.JSONObject;

public class MechManiaHTTP {
	private final static int HTTP_MAX_TIMEOUT_MILLISECONDS = 120000;  // 0 = Infinite, but we don't want to wait forever
	
	private String hostname;
	
	public MechManiaHTTP(String hostname) {
		this.hostname = hostname;
	}
	
	/**
	 * makeRequest - Make a GET request to the game HTTP server
	 * @param resource - The path on the HTTP server to the resource to request
	 * @return An HttpResponse object containing the HTTP status code and returned JSON
	 */
	public HTTPResponse makeRequest(String resource) throws GameOverException {
		try {
			JSONObject empty = new JSONObject();
			empty.append("empty", "empty");
			
			return makeRequest(resource, empty);
		} catch (JSONException e) {
			e.printStackTrace();
		}
		return null;
	}
	
	/**
	 * makeRequest - Make a POST request to the game HTTP server
	 * @param resource - The path on the HTTP server to the resource to request
	 * @param parameters
	 * @return An HttpResponse object containing the HTTP status code and returned JSON
	 */
	public HTTPResponse makeRequest(String resource, JSONObject parameters) throws GameOverException {
		URL url = null;
		HttpURLConnection urlconn = null;
		
		JSONObject jsonFromRequest = null;
		int responseCode = -1;
		
		try {
			url = new URL("http://" + hostname + resource);
			urlconn = ((HttpURLConnection)url.openConnection());
			
			urlconn.setReadTimeout(HTTP_MAX_TIMEOUT_MILLISECONDS);
			urlconn.setConnectTimeout(HTTP_MAX_TIMEOUT_MILLISECONDS);
			
			String encodedParams = parameters.toString();
			
			urlconn.setRequestMethod("POST"); // All requests require POST
			urlconn.setRequestProperty("Content-Length", ""+encodedParams.length());
			urlconn.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
			
			if (parameters.length() > 0) {  // POST-style request with JSON payload
				urlconn.setDoOutput(true);
				DataOutputStream dataOutputStream = new DataOutputStream(urlconn.getOutputStream());
				
				dataOutputStream.writeBytes(encodedParams);
				
				dataOutputStream.flush();
				dataOutputStream.close();
			}
			
			responseCode = urlconn.getResponseCode();
			
			jsonFromRequest = new JSONObject(readJsonStream(urlconn.getInputStream()));
			System.out.println(jsonFromRequest.toString());
		} catch (SocketException e) {
			// Do nothing, this probably came up because the server's lame
		} catch (MalformedURLException e) {
			e.printStackTrace();  // MUE extends IOE, but we might as well make sure we know what's thrown
		} catch (IOException e) {
			// We get IOEs from non-200 HTTP statuses, and we really don't care
			e.printStackTrace();
		} catch (JSONException e) {
			e.printStackTrace();
		}
		
		return new HTTPResponse(responseCode, jsonFromRequest);
	}

	/** 
	 * 
	 * 
	 * @param inputStream The input stream from an HTTP connection to read from.
	 * @return The JSON object sent back in the input stream
	 */
	private String readJsonStream(InputStream inputStream) {
		BufferedInputStream bis = new BufferedInputStream(inputStream);
		ByteArrayOutputStream bos = new ByteArrayOutputStream();
		
		int result = -1; 
		
		try {
			while ((result = bis.read())!= -1) {
				bos.write((byte)result);
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return bos.toString();
	}
	
}
