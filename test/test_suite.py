from server_tests import *
from random_tests import *
import unittest


def run_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestServer)
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(RandomTests))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = run_suite()
    runner.run (test_suite)
