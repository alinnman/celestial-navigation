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
from starfixdata_stat_1      import main as main_1
from starfixdata_stat_2      import main as main_2
from starfixdata_sea_1       import main as main_sea_1
from starfixdata_sea_2       import main as main_sea_2
from starfixdata_sea_3       import main as main_sea_3
from starfixdata_sea_4       import main as main_sea_4
from starfixdata_sea_5       import main as main_sea_5
from terrestrial             import main as main_terrestrial
from starfixdata_stat_1_mc   import main as main_1_mc
#pylint: enable=E0401

class TestStringMethods(unittest.TestCase):
    ''' Test class'''

    def test_starfix_1(self):
        ''' Test suite 1, Stationary '''
        main_1 ()

    def test_starfix_2(self):
        ''' Test suite 2, Stationary '''
        main_2 ()

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

if __name__ == '__main__':
    unittest.main()
