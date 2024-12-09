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

from starfixdata_stat_1 import main as main_1
from starfixdata_stat_2 import main as main_2
from starfixdata_sea    import main as main_sea
from terrestrial        import main as main_terrestrial

class TestStringMethods(unittest.TestCase):
    ''' Test class'''

    def test_starfix_1(self):
        ''' Test suite 1 '''
        main_1 ()

    def test_starfix_2(self):
        ''' Test suite 2 '''
        main_2 ()

    def test_sea (self):
        ''' Test suite for DR/Moving '''
        main_sea ()

    def test_terrestrial (self):
        ''' Test suite for Terrestrial '''
        main_terrestrial ()

if __name__ == '__main__':
    unittest.main()
