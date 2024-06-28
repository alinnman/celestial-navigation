from starfix import getCircleForAngle, getTerrestrialPosition, LatLon, getGoogleMapString 


# Simple sample of terrestrial navigation on three lighthouses. 

Landsort = LatLon (58.739439, 17.865486)
GustafDalen = LatLon (58.594091, 17.467489)
Hävringe = LatLon (58.60355, 17.316041)

EstimatedPosition = LatLon (58.4, 17.7)

Angle1 = 20
Angle2 = 45

p = getTerrestrialPosition (Hävringe, GustafDalen, Angle1, GustafDalen, Landsort, Angle2, EstimatedPosition)
print (getGoogleMapString(p,4))
