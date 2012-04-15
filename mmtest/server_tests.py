import unittest
import urllib2
import thread
from mm18.server.run import Main

class TestServer(unittest.TestCase):
    """
    Empty test file for testing future sever implementation
    """
    def setUp(self):
        pass

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
