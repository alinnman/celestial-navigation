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
     get_google_map_string, IntersectError, LatLonGeodetic

starttime = time ()

# Our starfix data

THE_POS = LatLonGeodetic (58, 18)

a = Sight (   object_name          = "Sun",
              set_time             = "2024-06-29 08:21:00+00:00",
              gha_time_0           = "299:6.6",
              gha_time_1           = "314:6.5",
              decl_time_0          = "23:11.6",
              decl_time_1          = "23:11.4",
              measured_alt         = "92:46",
              artificial_horizon   = True,
              estimated_position   = THE_POS
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


collection = SightCollection ([a, b, c])
try:
    intersections, fitness, diag_output =\
          collection.get_intersections (return_geodetic=True)
except IntersectError as ve:
    print ("Cannot perform a sight reduction. Bad sight data.")
    print ("Check the circles! " + collection.get_map_developers_string(geodetic=True))
    exit ()
endtime = time ()
takenMs = round((endtime-starttime)*1000,2)
print (get_representation(intersections,1))
assert isinstance (intersections, LatLonGeodetic)
print ("MD = " + collection.get_map_developers_string(geodetic=True, viewpoint=intersections))
print ("GM = " + get_google_map_string(intersections,4))

# Check azimuth
assert isinstance (intersections, LatLonGeodetic)
az = a.get_azimuth (intersections)
print ("Azimuth A = " + str(round(az,2)))
az = b.get_azimuth (intersections)
print ("Azimuth B = " + str(round(az,2)))
az = c.get_azimuth (intersections)
print ("Azimuth C = " + str(round(az,2)))


#Diagnostics for map rendering etc.
print ("Some useful data follows")

print ("A radius = " + str(round(a.get_circle(geodetic=True).get_radius (),1)))
print ("A GP     = " + get_google_map_string(LatLonGeodetic(ll=a.gp),4))

print ("B radius = " + str(round(b.get_circle(geodetic=True).get_radius (),1)))
print ("B GP     = " + get_google_map_string(LatLonGeodetic(ll=b.gp),4))

print ("C radius = " + str(round(c.get_circle(geodetic=True).get_radius (),1)))
print ("C GP     = " + get_google_map_string(LatLonGeodetic(ll=c.gp),4))

print ("Time taken = " +str(takenMs)+" ms")
