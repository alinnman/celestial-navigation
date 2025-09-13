''' Test suite for the toolkit '''
# pylint: disable=C0413
import unittest

import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

#pylint: disable=E0401
from starfixdata_stat_1      import main as main_1_mr
from starfixdata_stat_1_mc   import main as main_1_mc
from starfixdata_stat_2_na   import main as main_2
from starfixdata_stat_3      import main as main_3
from starfixdata_sea_1       import main as main_sea_1
from starfixdata_sea_2       import main as main_sea_2
from starfixdata_sea_3       import main as main_sea_3
from starfixdata_sea_4       import main as main_sea_4
from starfixdata_sea_5       import main as main_sea_5
from terrestrial             import main as main_terrestrial
from starfix                 import LatLonGeocentric, LatLonGeodetic, spherical_distance,\
                                    to_rectangular, to_latlon
#pylint: enable=E0401


try:
    sys.path.remove(str(parent))
except ValueError:
    pass

class TestStringMethods(unittest.TestCase):
    ''' Test class'''

    def test_starfix_1(self):
        ''' Test suite 1, Stationary '''
        main_1_mr ()

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

    def test_latlons (self):
        ''' 1. Verify that the D2C and C2D functions are inverses
            2. Checking accuracy of the mapping
            3. Some other accuracy checks
        '''

        # Known reference values
        # These values where picked from https://www.vcalc.com/wiki/geodetic-latitude
        test_cases = [
            # (geocentric_lat, expected_geodetic_lat in arcseconds, max_error_arcsec)
            (30.0, 108601.2),      # 30° - difference ~6.17 arcmin
            (45.0, 162691.2),      # 45° - difference ~11.6 arcmin (maximum)
            (60.0, 216597.6),      # 60° - difference ~9.95 arcmin
            (89.0, 320425.2),      # Near pole - small difference
        ]

        #print ("Testing D2C -> C2D")
        for x in range (0, 91):
            a = LatLonGeocentric (x,40)
            b = LatLonGeodetic (ll = a)
            #print (str(x) + ";" + str(b.get_lat()))
            c = b.get_latlon ()
            d = spherical_distance (a, c)
            #print ("Difference is " + str(d))
            assert d < 0.001

        #print ("Testing C2D -> D2C")
        for x in range (0, 91):
            a = LatLonGeodetic (x,40)
            b = a.get_latlon()
            #print (str(x) + ";" + str(b.get_lat()))
            c = LatLonGeodetic (ll = b)
            d = spherical_distance (a, c)
            #print ("Difference is " + str(d))
            assert d < 0.001

        for geocentric_lat, expected_geodetic_lat_as in test_cases:
            geocentric = LatLonGeocentric(geocentric_lat, 0.0)
            geodetic = LatLonGeodetic(ll=geocentric)
            error_arcsec = abs(geodetic.get_lat() - expected_geodetic_lat_as/3600) * 3600
            #print (error_arcsec)
            assert error_arcsec < 2.0

        x = LatLonGeocentric (lat = 30, lon = 40)
        y = to_rectangular (x)
        z = to_latlon (y)
        assert (abs(z.get_lat() - x.get_lat()) < 0.00000000000001)
        assert (abs(z.get_lon() - x.get_lon()) < 0.00000000000001)
        

