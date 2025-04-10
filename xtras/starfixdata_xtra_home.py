''' This is a real-world sample. Very basic sextant used 
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

from starfix import Sight, SightCollection, Sextant, Chronometer,\
                    get_decimal_degrees_from_tuple,\
                    get_representation, \
                    get_google_map_string,\
                    IntersectError, LatLonGeodetic,\
                    Circle
from calibration import calibrationRealValue, calibrationMeasuredValue

starttime = time ()

# This is observations from actual sextant readings.
# I used a simple plastic sextant (Davis Mk III) and an artificial horizon.

# Defining the Sextant object, using the calculated gradation error as parameter.
mySextant = Sextant (graduation_error=\
                     get_decimal_degrees_from_tuple (calibrationMeasuredValue) / \
                     get_decimal_degrees_from_tuple (calibrationRealValue),\
                     index_error=0)

# Defining the Chronometer object
myChronometer = Chronometer\
    (set_time                   = "2024-06-14 03:00:00+00:00",\
     set_time_deviation_seconds = 0,\
     drift_sec_per_day          = 0.3)

THE_POS = LatLonGeodetic (59, 18)

def get_starfixes (drp_pos : LatLonGeodetic):
    ''' Returns a list of used star fixes (SightCollection) '''

    s1 = Sight (   object_name             = "Sun",
                set_time                 = "2024-06-14 05:57:50+00:00",
                gha_time_0               = "254:54.8",
                gha_time_1               = "269:54.7",
                decl_time_0              = "23:17.1",
                decl_time_1              = "23:17.3",
                measured_alt             = "57:8",
                artificial_horizon       = True,
                index_error_minutes      = 0,
                limb_correction          = -1,
                sextant                  = mySextant,
                ##chronometer              = myChronometer,
                estimated_position       = drp_pos
                )

    s2 = Sight (   object_name             = "Sun",
                set_time                 = "2024-06-15 14:49:07+00:00",
                gha_time_0               = "29:50.4",
                gha_time_1               = "44:50.2",
                decl_time_0              = "23:20.5",
                decl_time_1              = "23:20.6",
                measured_alt             = "70:17",
                artificial_horizon       = True,
                index_error_minutes      = 0,
                sextant                  = mySextant,
                ##chronometer              = myChronometer
                )
    return SightCollection ([s1, s2])

def main ():
    ''' Main body of script.'''
    try:
        intersections, _, _, collection =\
                SightCollection.get_intersections_conv (return_geodetic=True,
                                                        estimated_position=THE_POS,
                                                        get_starfixes=get_starfixes,
                                                        limit=500)
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
    int_circle = Circle (intersections, 0.01)
    print ("INT = " + int_circle.get_map_developers_string(include_url_start=True))

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
 