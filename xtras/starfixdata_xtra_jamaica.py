''' This is a sample for celestial navigation for a stationary observer 
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)

'''
# pylint: disable=C0413
from time import time

import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

try:
    sys.path.remove(str(parent))
except ValueError:
    pass

from starfix import Sight, SightCollection, get_representation,\
     get_google_map_string, IntersectError, Sextant, LatLonGeodetic

# Defining the Sextant object.
mySextant = Sextant (index_error=0.5)

# Our starfix data
# Sample found in
# https://www.facebook.com/groups/148521952310126/permalink/1966017207227249/?rdid=ndpn9CqTjIZ8wsmT&share_url=https%3A%2F%2Fwww.facebook.com%2Fshare%2Fp%2F1B3UXbuZTS%2F

METER_PER_FEET = 0.3048
HEIGHT_IN_FEET = 16
TEMPERATURE    = 30

THE_POS = LatLonGeodetic (17.8, -76.7)

def get_starfixes (drp_pos : LatLonGeodetic) -> SightCollection :
    ''' Returns a list of used star fixes (SightCollection) '''

    a = Sight (   object_name          = "Venus",
                set_time             = "2024-12-28 22:45:10+00:00",
                gha_time_0           = "100:37.6",
                gha_time_1           = "115:37.5",
                decl_time_0          = "-14:54.6",
                decl_time_1          = "-14:53.5",
                measured_alt         = "42:19.4",
                observer_height      = HEIGHT_IN_FEET * METER_PER_FEET,
                sextant              = mySextant,
                temperature          = TEMPERATURE,
                pressure             = 101.2,
                estimated_position   = drp_pos
                )

    b = Sight (   object_name          = "Jupiter",
                set_time             = "2024-12-28 22:53:41+00:00",
                gha_time_0           = "355:36.9",
                gha_time_1           = "10:39.6",
                decl_time_0          = "21:49.1",
                measured_alt         = "26:50.8",
                observer_height      = HEIGHT_IN_FEET * METER_PER_FEET,
                sextant              = mySextant,
                index_error_minutes  = -5.4,
                no_dip               = True,
                temperature          = TEMPERATURE,
                pressure             = 101.2
                )

    c = Sight (   object_name          = "Rigel",
                set_time             = "2024-12-28 23:00:41+00:00",
                gha_time_0           = "82:54.1",
                gha_time_1           = "97:56.6",
                decl_time_0          = "-8:10.4",
                sha_diff             = "281:3.6",
                measured_alt         = "13:52.4",
                observer_height      = HEIGHT_IN_FEET * METER_PER_FEET,
                sextant              = mySextant,
                temperature          = TEMPERATURE,
                pressure             = 101.2
                )

    d = Sight (   object_name          = "Achernar",
                set_time             = "2024-12-28 23:04:39+00:00",
                gha_time_0           = "82:54.1",
                gha_time_1           = "97:56.6",
                decl_time_0          = "-57:6.9",
                sha_diff             = "335:20.0",
                measured_alt         = "13:40.1",
                observer_height      = HEIGHT_IN_FEET * METER_PER_FEET,
                sextant              = mySextant,
                temperature          = TEMPERATURE,
                pressure             = 101.2
                )

    e = Sight (   object_name          = "Saturn",
                set_time             = "2024-12-28 23:07:06+00:00",
                gha_time_0           = "96:35.4",
                gha_time_1           = "111:37.7",
                decl_time_0          = "-8:0.6",
                decl_time_1          = "-8:0.5",
                measured_alt         = "56:28.8",
                observer_height      = HEIGHT_IN_FEET * METER_PER_FEET,
                sextant              = mySextant,
                temperature          = TEMPERATURE,
                pressure             = 101.2
                )

    f = Sight (   object_name          = "Polaris",
                set_time             = "2024-12-28 23:10:49+00:00",
                gha_time_0           = "82:54.1",
                gha_time_1           = "97:56.6",
                decl_time_0          = "89:22.4",
                sha_diff             = "313:42.3",
                measured_alt         = "18:37.1",
                observer_height      = HEIGHT_IN_FEET * METER_PER_FEET,
                sextant              = mySextant,
                index_error_minutes  = -7.1,
                no_dip               = True,
                temperature          = TEMPERATURE,
                pressure             = 101.2
                )
    return SightCollection ([a, b, c, d, e, f])

def main ():
    ''' Main body of script.'''

    starttime = time ()

    try:
        intersections, _, _, collection =\
              SightCollection.get_intersections_conv (return_geodetic=True,
                                                      estimated_position=THE_POS,
                                                      get_starfixes=get_starfixes)
    except IntersectError as ve:
        print ("Cannot perform a sight reduction. Bad sight data.\n" + str(ve))
        if ve.coll_object is not None:
            if isinstance (ve.coll_object, SightCollection):
                print ("Check the circles! " +
                        ve.coll_object.get_map_developers_string(geodetic=True))
        exit ()

    assert intersections is not None
    assert collection is not None
    endtime = time ()
    taken_ms = round((endtime-starttime)*1000,3)
    print (get_representation(intersections,1))
    assert isinstance (intersections, LatLonGeodetic)
    # print ("MD = " + collection.get_map_developers_string(geodetic=True, viewpoint=intersections))
    print ("GM = " + get_google_map_string(intersections,4))

    # Check azimuth
    assert isinstance (intersections, LatLonGeodetic)
    counter = 0
    for s in collection.sf_list:
        counter += 1
        az = s.get_azimuth (intersections)
        print ("Azimuth " + str(counter) + " = " + str(round(az,2)))

    #Diagnostics for map rendering etc.
    print ("Some useful data follows")
    counter = 0
    for s in collection.sf_list:
        counter += 1
        print (str(counter) + " radius = " +\
                str(round(s.get_circle(geodetic=True).get_radius (),1)))
        print (str(counter) + " GP     = " +\
                get_google_map_string(LatLonGeodetic(ll=s.get_gp()),4))

    print ("Time taken = " +str(taken_ms)+" ms")

if __name__ == '__main__':
    main()
