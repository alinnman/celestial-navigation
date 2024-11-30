''' Test suite for the toolkit '''

import unittest
from starfixdata_stat_1 import main

class TestStringMethods(unittest.TestCase):
    ''' Test class'''

    def test_starfix(self):
        ''' Test suite'''
        main ()

if __name__ == '__main__':
    unittest.main()
