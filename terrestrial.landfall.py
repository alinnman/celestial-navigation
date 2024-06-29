from starfix import getCircleForAngle, getTerrestrialPosition, LatLon, getGoogleMapString, degToRad, EARTH_RADIUS


# Simple sample of terrestrial navigation on three lighthouses. 

# Our three lighthouses
Landsort = LatLon (58.739439, 17.865486)
GustafDalen = LatLon (58.594091, 17.467489)
Hävringe = LatLon (58.60355, 17.316041)

Angle1 = 20
Angle2 = 45

p, c1, r1, c2, r2 = getTerrestrialPosition (Hävringe, GustafDalen, Angle1, GustafDalen, Landsort, Angle2)
print ("Your location 1 = " + getGoogleMapString(p[0],4))
print ("Your location 2 = " + getGoogleMapString(p[1],4))


print ("========================")
print ("Centerpoint 1 = " + getGoogleMapString (c1, 4))
print ("Radius 1 = " + str(degToRad(r1)*EARTH_RADIUS))
print ("Centerpoint 2 = " + getGoogleMapString (c2, 4))
print ("Radius 2 = " + str(degToRad(r2)*EARTH_RADIUS))

'''
Link to intersections
https://www.mapdevelopers.com/draw-circle-tool.php?circles=%5B%5B12922.53%2C58.4904%2C17.3669%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B19890.51%2C58.5634%2C17.8054%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1000%2C58.6033323%2C17.3136798%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1000%2C58.5941%2C17.4674833%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B1000%2C58.7395979%2C17.8656699%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%5D
'''

