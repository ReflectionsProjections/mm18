#! /usr/bin/env python

from mmtest.server_tests import *
import unittest

def get_suite():
	suite = unittest.TestLoader().loadTestsFromTestCase(TestServer)
	return suite

def run_suite():
	runner = unittest.TextTestRunner()
	suite = get_suite()
	return runner.run(suite)

if __name__ == '__main__':
	run_suite()
