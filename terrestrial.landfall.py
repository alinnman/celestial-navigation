''' Simple sample for terrestrial navigation (landfall) 
    (C) August Linnman, 2024, email: august@linnman.net
    MIT License (see LICENSE file)

'''

from starfix import get_terrestrial_position, LatLon,\
      get_google_map_string, deg_to_rad, EARTH_RADIUS

# Simple sample of terrestrial navigation on three lighthouses.

# Our three lighthouses
Landsort = LatLon (58.739439, 17.865486)
GustafDalen = LatLon (58.594091, 17.467489)
Havringe = LatLon (58.60355, 17.316041)

ANGLE_1 = 20
ANGLE_2 =  45

p, c1, r1, c2, r2 =\
      get_terrestrial_position (Havringe, GustafDalen, ANGLE_1, GustafDalen, Landsort, ANGLE_2)
print ("Your location 1 = " + get_google_map_string(p[0],4))
print ("Your location 2 = " + get_google_map_string(p[1],4))


print ("========================")
print ("Centerpoint 1 = " + get_google_map_string (c1, 4))
print ("Radius 1 = " + str(deg_to_rad(r1)*EARTH_RADIUS))
print ("Centerpoint 2 = " + get_google_map_string (c2, 4))
print ("Radius 2 = " + str(deg_to_rad(r2)*EARTH_RADIUS))


#Link to intersections
#https://www.mapdevelopers.com/draw-circle-tool.php?circles=%5B%5B12922.53%2C58.4904%2C17.3669%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B19890.51%2C58.5634%2C17.8054%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1000%2C58.6033323%2C17.3136798%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1000%2C58.5941%2C17.4674833%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1000%2C58.7395979%2C17.8656699%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%5D
