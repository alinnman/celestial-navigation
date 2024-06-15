from starfix import angleBetweenPoints, getDMS, LatLon

mountain = LatLon (59.31994768792838, 18.050803976905534)
scienceTower = LatLon (59.401619602468514, 17.9463822774136)
riddarholmen = LatLon (59.32481913898507, 18.064878270190704)

print ("Angle is " + str(getDMS(angleBetweenPoints(mountain, scienceTower, riddarholmen))))
