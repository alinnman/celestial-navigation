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

#METER_PER_FEET = 0.3048
#HEIGHT_IN_FEET = 16
#TEMPERATURE    = 30

THE_POS = LatLonGeodetic (17.8, -76.7)

def get_starfixes (drp_pos : LatLonGeodetic) -> SightCollection :
    ''' Returns a list of used star fixes (SightCollection) '''

    a = Sight (   object_name          = "Sun",
                set_time             = "2024-06-29 08:21:00+00:00",
                gha_time_0           = "299:6.6",
                gha_time_1           = "314:6.5",
                decl_time_0          = "23:11.6",
                decl_time_1          = "23:11.4",
                measured_alt         = "92:46",
                artificial_horizon   = True,
                estimated_position   = drp_pos
                )

    b = Sight (   object_name          = "Sun",
                set_time             = "2024-06-29 12:51:00+00:00",
                gha_time_0           = "359:6.1",
                gha_time_1           = "14:6.6",
                decl_time_0          = "23:11.1",
                decl_time_1          = "23:10.8",
                measured_alt         = "98:36",
                artificial_horizon   = True
                )

    c = Sight (   object_name          = "Sun",
                set_time             = "2024-06-28 15:36:00+00:00",
                gha_time_0           = "44:5.7",
                gha_time_1           = "59:5.6",
                decl_time_0          = "23:10.5",
                decl_time_1          = "23:10.4",
                measured_alt         = "58:40",
                artificial_horizon   = True
                )
    return SightCollection ([a, b, c])

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
    print ("MD = " + collection.get_map_developers_string(geodetic=True, viewpoint=intersections))
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
                get_google_map_string(LatLonGeodetic(ll=s.gp),4))

    print ("Time taken = " +str(taken_ms)+" ms")

if __name__ == '__main__':
    main()
