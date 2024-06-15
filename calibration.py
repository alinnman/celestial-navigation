from starfix import angleBetweenPoints, getDMS, LatLon

mountain = LatLon (59.319946870523125, 18.05080784094633)
scienceTower = LatLon (59.40167156189403, 17.94701732894245)
westerTowerEastWall = LatLon (59.34574503565645, 18.033482004389334)
riddarholmen = LatLon (59.32481913898507, 18.064878270190704)
kaknäs = LatLon(59.33503259537072, 18.12680035827089)

print ("Angle is " + str(getDMS(angleBetweenPoints(mountain, westerTowerEastWall, kaknäs))))
