from starfix import getCircleForAngle, getTerrestrialPosition, LatLon 

### Temporary testing

q = getCircleForAngle (LatLon (59,18), LatLon (60,19), 50)
print (str(q[0]) + ";" + str(q[1]))
p = getTerrestrialPosition (LatLon (59,18), LatLon (60,19), 5, LatLon (60,19), LatLon(60,20), 4, estimatedPosition = LatLon (54, 19))
print (str(p))
#print (type(p))
#print (str(p[0]) + ";" + str(p[1]))