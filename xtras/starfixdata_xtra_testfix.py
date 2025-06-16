''' This is a sample for celestial navigation for a stationary observer 
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)

    Test sample from sextant exercise. This used a Ho observation so I added
    support for this in the code (eliminating refraction and dip calculations)
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
     get_google_map_string, IntersectError, LatLonGeodetic

# Our starfix data

TEMPERATURE = 18

THE_POS = LatLonGeodetic (-34, 18)


def get_starfixes (drp_pos : LatLonGeodetic):
    ''' Get a collection of starfixes (sights) '''
    a = Sight (   object_name          = "Sabik",
                set_time             = "2024-10-01 17:13:00+00:00",
                gha_time_0           = "265:55.1",
                gha_time_1           = "280:57.5",
                decl_time_0          = "-15:45.3",
                sha_diff             = "102:3.2",
                measured_alt         = "57:36.8",
                observer_height      = 2.5,
                temperature          = TEMPERATURE,
                ho_obs               = True,
                estimated_position   = drp_pos
                )

    b = Sight (   object_name          = "Venus",
                set_time             = "2024-10-01 17:13:00+00:00",
                gha_time_0           = "47:57.8",
                gha_time_1           = "62:57.3",
                decl_time_0          = "-15:14.8",
                decl_time_1          = "-15:15.9",
                measured_alt         = "25:8.4",
                observer_height      = 2.5,
                temperature          = TEMPERATURE,
                ho_obs               = True
                )

    c = Sight (   object_name          = "Saturn",
                set_time             = "2024-10-01 17:13:00+00:00",
                gha_time_0           = "279:30.9",
                gha_time_1           = "294:33.5",
                decl_time_0          = "-8:11.8",
                measured_alt         = "30:20.2",
                observer_height      = 2.5,
                temperature          = TEMPERATURE,
                ho_obs               = True
                )
    return SightCollection ([a, b, c])

def main ():
    ''' Main function of module. '''
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
