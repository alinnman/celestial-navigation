from starfix import angleBetweenPoints, getDMS, LatLon

mountain = LatLon (59.319946870523125, 18.05080784094633)
hyllan = LatLon (59.32062936826502, 18.046798890457488)
scienceTower = LatLon (59.40167156189403, 17.94701732894245)
westerTowerEastWall = LatLon (59.34574443361814, 18.033477910104178)
riddarholmen = LatLon (59.32481913898507, 18.064878270190704)
kaknäs = LatLon(59.33503270844517, 18.126800449743094)


calibrationRealValue = getDMS(angleBetweenPoints(hyllan, westerTowerEastWall, kaknäs))

print ("Angle is " + str(calibrationRealValue))

calibrationMeasuredValue = (85, 54, 0)

