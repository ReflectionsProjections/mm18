import unittest
import urllib, urllib2
import thread
import logging
from mm18.server.run import Main

class TestServer(unittest.TestCase):
	"""
	Tests for the server.  Validation of HTTP/REST and JSON should all
	go here
	"""

	@classmethod
	def setUpClass(cls):
		args = ()
		kwargs = {'log_file': 'Server.log',
				'log_format': '%(levelname)s: %(message)s',
				'log_level': logging.INFO}
		server_thread = thread.start_new_thread(Main, ())

	def testEcho(self):
		"""Iterates through the different HTTP codes and tests the server's
		ability to echo them back.
		"""
		http_codes = [200, 400, 401, 403, 404, 405, 418, 429, 500, 501]
		for code in http_codes:
			try:
				conn = urllib2.urlopen('http://localhost:6969/api/tests/echo/'+str(code))
				self.assertEqual(code, conn.getcode())
				conn.close()
			except urllib2.HTTPError, e:
				self.assertEqual(e.getcode(), code)

	def test404(self):
		"""Tries to access an invalid path and checks to make sure the 
		server returns a HTTP 404 error.
		"""
		bad_url = "/bad/path/not/in/url/patterns/"
		try:
			conn = urllib2.urlopen('http://localhost:6969' + bad_url)
			code = conn.getcode()
			conn.close()
		except urllib2.HTTPError, e:
			code = e.code
		self.assertEqual(404, code)
	
	def test405(self):
		"""Tries to access a valid url with a bad method, expecting
		a HTTP 405 error in response.
		"""
		try:
			conn = urllib2.urlopen('http://localhost:6969/api/tests/post')
			code = conn.getcode()
			conn.close()
		except urllib2.HTTPError, e:
			code = e.code
		self.assertEqual(405, code)
		try:
			data = urllib.urlencode({})
			conn = urllib2.urlopen('http://localhost:6969/api/tests/echo/200', data)
			code = conn.getcode()
			conn.close()
		except urllib2.HTTPError, e:
			code = e.code
		self.assertEqual(405, code)

	def test400(self):
		""" Tests to make sure the server throws a 400 error if given invalid JSON
		"""
		try:
			data = urllib.urlencode({})
			header = {"Content-type": "application/json"}
			req = urllib2.Request('http://localhost:6969/api/tests/post', data, header)
			conn = urllib2.urlopen(req)
			code = conn.getcode()
			respnse = conn.read()
			conn.close()
		except urllib2.HTTPError, e:
			code = e.code
		self.assertEqual(400, code)

	def testEcho(self):
		server_thread = thread.start_new_thread(Main, ())
		http_codes = [200, 400, 401, 403, 404, 405, 418, 429, 500, 501]
		for code in http_codes:
			try:
				conn = urllib2.urlopen('http://localhost:6969/api/tests/echo/' + str(code))
				self.assertEqual(code, conn.getcode())
				conn.close()
			except urllib2.HTTPError, e:
				self.assertEqual(e.getcode(), code)
