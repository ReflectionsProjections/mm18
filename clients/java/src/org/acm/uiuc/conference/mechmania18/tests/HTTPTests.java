package org.acm.uiuc.conference.mechmania18.tests;

import junit.framework.Assert;

import org.acm.uiuc.conference.mechmania18.net.*;
import org.json.JSONException;
import org.json.JSONObject;
import org.junit.Before;
import org.junit.Test;

/**
 * Unit tests for the HTTP-related classes.  Requires connection to the Internet
 * for a successful test.
 * 
 * @author Nick
 *
 */
public class HTTPTests {
	MechManiaHTTP zippopotamus;
	HTTPResponse zippopotamusresponse;
	MechManiaHTTP google;
	
	@Before
	public void initialize() {
		zippopotamus = new MechManiaHTTP("zippopotam.us", 80);
		google = new MechManiaHTTP("google.com", 80);
		zippopotamusresponse = zippopotamus.makeRequest("/us/61801");
	}
	
	@Test
	public void get200OK() {
		Assert.assertEquals(200, zippopotamusresponse.getStatusCode());
	}
	
	@Test
	public void get404NotFound() {
		HTTPResponse response = google.makeRequest("/obvious404.bad");
		
		Assert.assertEquals(404, response.getStatusCode());
	}
	
	@Test
	public void getInvalidJSON() {
		HTTPResponse response = google.makeRequest("/");
		
		Assert.assertNull(response.getResponse());
	}
	
	@Test
	public void getValidJSON() {
		JSONObject json = zippopotamusresponse.getResponse();
		
		Assert.assertFalse(json.isNull("post code"));
		Assert.assertFalse(json.isNull("country"));
		Assert.assertFalse(json.isNull("country abbreviation"));
		Assert.assertFalse(json.isNull("places"));
		
		try {
			Assert.assertEquals("61801", json.getString("post code"));
			Assert.assertEquals("US", json.getString("country abbreviation"));
			Assert.assertEquals("United States", json.getString("country"));
		} catch (JSONException e) {
			Assert.fail("Unable to parse JSON");
		}
	}
	
	
}
