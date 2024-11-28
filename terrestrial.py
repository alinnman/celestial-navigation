''' Simple sample for terrestrial navigation (landfall) 
    © August Linnman, 2024, email: august@linnman.net
    MIT License (see LICENSE file)

'''
from time import time
from starfix import get_terrestrial_position, LatLon,\
      get_google_map_string, deg_to_rad, EARTH_RADIUS

starttime = time ()

# Simple sample of terrestrial navigation on three lighthouses.

# Our three lighthouses
P1 = LatLon (58.739439, 17.865486)
P2 = LatLon (58.594091, 17.467489)
P3 = LatLon (58.60355, 17.316041)

ANGLE_1 = 20
ANGLE_2 = 45

p, c1, r1, c2, r2, fitness, diag_output  =\
      get_terrestrial_position (P3, P2, ANGLE_1, P2, P1, ANGLE_2)
assert isinstance (p, tuple)
print ("Your location 1 = " + get_google_map_string(p[0],4))
print ("Your location 2 = " + get_google_map_string(p[1],4))


print ("========================")
print ("Centerpoint 1 = " + get_google_map_string (c1, 4))
print ("Radius 1 = " + str(deg_to_rad(r1)*EARTH_RADIUS))
print ("Centerpoint 2 = " + get_google_map_string (c2, 4))
print ("Radius 2 = " + str(deg_to_rad(r2)*EARTH_RADIUS))

endtime = time ()
takenMs = round((endtime-starttime)*1000,2)
print ("Time taken = " +str(takenMs)+" ms")
