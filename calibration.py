from starfix import angleBetweenPoints, getDMS, LatLon

berget = LatLon (59.31994768792838, 18.050803976905534)
scienceTower = LatLon (59.401619602468514, 17.9463822774136)
johannes = LatLon (59.33945487100022, 18.06470993954498)

print ("Angle is " + str(getDMS(angleBetweenPoints(berget, scienceTower, johannes))))
