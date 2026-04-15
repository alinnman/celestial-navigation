'''
Simple test script for the solution described in 
https://github.com/alinnman/celestial-navigation/discussions/43 
'''
from math import atan2, asin, sin, cos, sqrt, pi
from starfix import LatLonGeocentric, deg_to_rad, rad_to_deg, get_mr_item,\
                    ObsTypes, parse_angle_string

def get_latlon_for_solar_obs (solar_azimuth : float, solar_altitude : float,
                              timestamp : str) -> list[LatLonGeocentric] :
    ''' This function returns a list of possible latlons based on the 
        observations in the parameters. 
        NOTE: The function uses the starfix nautical almanac to get the SHA and DECL
        values for the Sun
    '''
    # Check parameters
    assert (solar_azimuth >= 0.0 and solar_azimuth <= 360.0)
    assert (solar_altitude >= 0.0 and solar_altitude <= 90.0)
    # Convert to radians
#pylint: disable=C0103
    A = deg_to_rad (solar_azimuth)
    alpha = deg_to_rad (solar_altitude)
    # Get astrometric data
    GHA   = get_mr_item ("Sun", timestamp, ObsTypes.GHA)
    delta = get_mr_item ("Sun", timestamp, ObsTypes.DECL)

    GHA   = deg_to_rad(parse_angle_string (GHA))
    delta = deg_to_rad(parse_angle_string (delta))


    # Latitude calculation
    a = sin(alpha)
    b = cos(alpha) * cos(A)
    c = sin(delta)

    R = sqrt(a**2 + b**2)
    assert abs (c) <= R
    asin_term = asin (c/R)
    theta = atan2 (b,a)

    phi_candidates = [asin_term - theta, (pi - asin_term) - theta]

    results = []
    for phi in phi_candidates:
        # Normalize phi to [-pi, pi]
        phi = (phi + pi) % (2 * pi) - pi
        # Check if latitude is physically valid [-90, 90]
        if abs(phi) <= pi/2:
            # 2. Solve for Local Hour Angle (H)
            y = -sin(A) * cos(alpha)
            x = sin(alpha) * cos(phi) - cos(alpha) * sin(phi) * cos(A)

            H = atan2(y, x)

            # 3. Solve for Longitude (lambda)
            lon_rad = H - GHA

            # Normalize Longitude to [-pi, pi]
            lon_rad = (lon_rad + pi) % (2 * pi) - pi

            results.append((LatLonGeocentric(rad_to_deg(phi), rad_to_deg(lon_rad))))
#pylint: enable=C0103
    return results

result = get_latlon_for_solar_obs (solar_azimuth=138, solar_altitude=14.6,
                                   timestamp="2026-03-02 08:00:00")
for r in result:
    print (r)
