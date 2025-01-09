''' This is a sample for celestial navigation for a stationary observer 
    © August Linnman, 2024, email: august@linnman.net
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
     get_google_map_string, IntersectError


starttime = time ()

# Our starfix data

TEMPERATURE = 18

a = Sight (   object_name          = "Sabik",
              set_time             = "2024-10-01 17:13:00+00:00",
              gha_time_0           = "265:55.1",
              gha_time_1           = "280:57.5",
              decl_time_0          = "-15:45.3",
              sha_diff             = "102:3.2",
              measured_alt         = "57:36.8",
              observer_height      = 2.5,
              temperature          = TEMPERATURE,
              ho_obs               = True
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

collection = SightCollection ([a, b, c])
try:
    intersections, fitness, diag_output =\
        collection.get_intersections (limit=100)
except IntersectError as ve:
    print ("Cannot perform a sight reduction. Bad sight data.")
    print ("Check the circles! " + collection.get_map_developers_string())
    exit ()
endtime = time ()
takenMs = round((endtime-starttime)*1000,2)
print (get_representation(intersections,1))
print ("MD = " + collection.get_map_developers_string())
print ("GM = " + get_google_map_string(intersections,4))

#Diagnostics for map rendering etc.
print ("Some useful data follows")
print ("A radius = " + str(round(a.get_radius (),1)))
print ("A GP     = " + get_google_map_string(a.gp,4))

print ("B radius = " + str(round(b.get_radius (),1)))
print ("B GP     = " + get_google_map_string(b.gp,4))

print ("C radius = " + str(round(c.get_radius (),1)))
print ("C GP     = " + get_google_map_string(c.gp,4))

print ("Time taken = " +str(takenMs)+" ms")
