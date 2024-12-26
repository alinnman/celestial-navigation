''' This is a real-world sample. Very basic sextant used 
    © August Linnman, 2024, email: august@linnman.net
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

from starfix import Sight, SightCollection, LatLon, Sextant, Chronometer,\
                    get_decimal_degrees_from_tuple,\
                    get_representation, \
                    get_google_map_string, distance_between_points,\
                    IntersectError
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

S1 = Sight (   object_name          = "Sun", \
              set_time             = "2024-06-14 05:57:50+00:00", \
              gha_time_0           = "254:54.8", \
              gha_time_1           = "269:54.7", \
              decl_time_0          = "23:17.1", \
              decl_time_1          = "23:17.3", \
              measured_alt         = "57:8", \
              artificial_horizon   = True,\
              index_error_minutes  = 0,\
              semi_diameter_correction = 15.7,\
              sextant = mySextant,\
              chronometer = myChronometer
              )

S2 = Sight (   object_name          = "Sun", \
              set_time             = "2024-06-15 14:49:07+00:00", \
              gha_time_0           = "29:50.4", \
              gha_time_1           = "44:50.2", \
              decl_time_0          = "23:20.5", \
              decl_time_1          = "23:20.6", \
              measured_alt         = "70:17", \
              artificial_horizon   = True,\
              index_error_minutes  = 0,\
              sextant = mySextant,\
              chronometer = myChronometer
              )

collection = SightCollection ([S1, S2])

# This is the exact position of my observation location
home = LatLon (59.318659676810654, 18.04959717835501)

try:
    intersections, fitness, diag_output =\
        collection.get_intersections (estimated_position = LatLon(59,19))
except IntersectError as ve:
    print ("Cannot perform a sight reduction. Bad sight data.")
    exit ()

endtime = time ()
takenMs = round((endtime-starttime)*1000,2)
assert isinstance (intersections, LatLon)
print (get_representation(intersections,1))
print ("MD = " + collection.get_map_developers_string())
print ("GM = " + get_google_map_string(intersections,4))
print ("Intersection distance from home = " + str(distance_between_points(intersections, home)))

#Diagnostics for map rendering etc.
print ("Some useful data follows")

print ("S1 radius = " + str(round(S1.get_radius (),1)))
print ("S1 GP     = " + get_google_map_string(S1.gp,4))
print ("Diff     = " + str(S1.get_distance_from (home)))
print ("--")

print ("S2 radius = " + str(round(S2.get_radius (),1)))
print ("S2 GP     = " + get_google_map_string(S2.gp,4))
print ("Diff     = " + str(S2.get_distance_from (home)))
print ("--")
print ("-----------------------------------")

print ("Time taken = " +str(takenMs)+" ms")
 