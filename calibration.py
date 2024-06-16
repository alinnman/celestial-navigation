from starfix import angleBetweenPoints, getDMS, LatLon

hyllan = LatLon (59.32062936826502, 18.046798890457488)
westerTowerEastWall = LatLon (59.34574443361814, 18.033477910104178)
kaknäs = LatLon(59.33503270844517, 18.126800449743094)

calibrationRealValue = getDMS(angleBetweenPoints(hyllan, westerTowerEastWall, kaknäs))
calibrationMeasuredValue = (85, 56, 0)

