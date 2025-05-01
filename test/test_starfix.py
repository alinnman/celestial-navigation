#!/usr/bin/env python3.11

''' Test suite for the toolkit '''
# pylint: disable=C0413
import unittest

import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

try:
    sys.path.remove(str(parent))
except ValueError:
    pass

#pylint: disable=E0401
from starfixdata_stat_1      import main as main_1_mr
from starfixdata_stat_1_na   import main as main_1
from starfixdata_stat_1_mc   import main as main_1_mc
from starfixdata_stat_2_na   import main as main_2
from starfixdata_stat_2      import main as main_2_mr
from starfixdata_stat_3      import main as main_3
from starfixdata_sea_1       import main as main_sea_1
from starfixdata_sea_2       import main as main_sea_2
from starfixdata_sea_3       import main as main_sea_3
from starfixdata_sea_4       import main as main_sea_4
from starfixdata_sea_5       import main as main_sea_5
from terrestrial             import main as main_terrestrial
from starfix                 import LatLonGeocentric, LatLonGeodetic, spherical_distance

#pylint: enable=E0401

class TestStringMethods(unittest.TestCase):
    ''' Test class'''

    def test_starfix_1(self):
        ''' Test suite 1, Stationary '''
        main_1 ()

    def test_starfix_2(self):
        ''' Test suite 2, Stationary '''
        main_2 ()

    def test_starfix_3(self):
        ''' Test suite 3, Stationary '''
        main_3 ()

    def test_sea_1 (self):
        ''' Test suite 1, for DR/Moving '''
        main_sea_1 ()

    def test_sea_2 (self):
        ''' Test suite 2, for DR/Moving '''
        main_sea_2 ()

    def test_sea_3 (self):
        ''' Test suite 3, for DR/Moving '''
        main_sea_3 ()

    def test_sea_4 (self):
        ''' Test suite 4, for DR/Moving '''
        main_sea_4 ()

    def test_sea_5 (self):
        ''' Test suite 4, for DR/Moving '''
        main_sea_5 ()

    def test_terrestrial (self):
        ''' Test suite for Terrestrial '''
        main_terrestrial ()

    def test_mc (self):
        ''' Test suite for Monte Carlo simulation '''
        main_1_mc ()

    def test_mr_1 (self):
        ''' Test suite for Machine-Readable Nautical Almanac '''
        main_1_mr ()

    def test_mr_2 (self):
        ''' Test suite for Machine-Readable Nautical Almanac '''
        main_2_mr ()

    def test_latlons (self):
        ''' Verify that the D2C and C2D functions are inverses '''
        for x in range (0, 91):
            a = LatLonGeocentric (x,40)
            b = LatLonGeodetic (ll = a)
            c = b.get_latlon ()
            d = spherical_distance (a, c)
            assert d < 0.001

if __name__ == '__main__':
    unittest.main()
