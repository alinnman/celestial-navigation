''' © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)

    Just a sample showing a simple sextant calibration '''

from starfix import angle_between_points, get_dms, LatLon

hyllan = LatLon (59.32062936826502, 18.046798890457488)
westerTowerEastWall = LatLon (59.34574443361814, 18.033477910104178)
kaknas = LatLon(59.33503270844517, 18.126800449743094)

calibrationRealValue = get_dms(angle_between_points(hyllan, westerTowerEastWall, kaknas))
calibrationMeasuredValue = (85, 56, 0)
