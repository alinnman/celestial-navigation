''' This is a sample for celestial navigation for a stationary observer 
    Sample taken from FB discussion with Nigel Coey. 
    Data is approximate star fixes from Macquarie Island
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)
    
Output: 
MEAN VALUE COORDINATE from multi-point sight data.
Location = (S 56°,50.2′;E 154°,27.0′)
Google Map coordinate = -56.84,154.45
https://www.mapdevelopers.com/draw-circle-tool.php?circles=%5B%5B5563507%2C-63.2367%2C39.3583%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B7790847%2C-52.7017%2C-51.5033%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B4450597%2C-57.1067%2C-122.9567%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%5D

Some useful data follows (Small circles of equal altitude). For plotting in map software etc.
A celestial body = Acrux
A radius = 5563.5
A GP     = -63.2367,39.3583

B celestial body = Canopus
B radius = 7790.8
B GP     = -52.7017,-51.5033

C celestial body = Achernar
C radius = 4450.6
C GP     = -57.1067,-122.9567

Map output: 
https://www.mapdevelopers.com/draw-circle-tool.php?circles=%5B%5B5563500%2C-62.7633%2C39.3583%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B7790800%2C-51.2983%2C-51.5033%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B4450600%2C-56.8933%2C-122.9567%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%5D 
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

THE_POS = LatLonGeodetic (-57, 154)

a = Sight (   object_name          = "Acrux",
              set_time             = "2024-08-31 11:10+00:00",
              gha_time_0           = "145:7",
              gha_time_1           = "160:9.4",
              decl_time_0          = "-63:14.2",
              measured_alt         = "40",
              sha_diff             = "173:1.1",
              estimated_position   = THE_POS
              )

b = Sight (   object_name          = "Canopus",
              set_time             = "2024-08-31 11:10+00:00",
              gha_time_0           = "145:7",
              gha_time_1           = "160:9.4",
              decl_time_0          = "-52:42.1",
              measured_alt         = "20",
              sha_diff             = "263:52.8"
              )

c = Sight (   object_name          = "Achernar",
              set_time             = "2024-08-31 11:10+00:00",
              gha_time_0           = "145:7",
              gha_time_1           = "160:9.4",
              decl_time_0          = "-57:6.4",
              measured_alt         = "50",
              sha_diff             = "335:20"
              )


collection = SightCollection ([a, b, c])
try:
    intersections, fitness, diag_output =\
          collection.get_intersections (limit=500, return_geodetic=True)
except IntersectError as ve:
    print ("Cannot perform a sight reduction. Bad sight data.")
    print ("Check the circles! " + collection.get_map_developers_string(geodetic=True))
    exit ()
endtime = time ()
takenMs = round((endtime-starttime)*1000,2)
print ("Location = " + get_representation(intersections,1))
print ("GM = " + get_google_map_string (intersections,2))
print ("MD = " + collection.get_map_developers_string(geodetic=True))

#Diagnostics for map rendering etc.
print ("")
print ("Some useful data follows (Small circles of equal altitude). \
       For plotting in map software etc.")
print ("A celestial body = " + a.object_name)
print ("A radius = " + str(round(a.get_circle(geodetic=True).get_radius (),1)))
print ("A GP     = " + get_google_map_string(LatLonGeodetic(ll=a.gp),4))
print ("")
print ("B celestial body = " + b.object_name)
print ("B radius = " + str(round(b.get_circle(geodetic=True).get_radius (),1)))
print ("B GP     = " + get_google_map_string(LatLonGeodetic(ll=b.gp),4))
print ("")
print ("C celestial body = " + c.object_name)
print ("C radius = " + str(round(c.get_circle(geodetic=True).get_radius (),1)))
print ("C GP     = " + get_google_map_string(LatLonGeodetic(ll=c.gp),4))



print ("Time taken = " +str(takenMs)+" ms")
