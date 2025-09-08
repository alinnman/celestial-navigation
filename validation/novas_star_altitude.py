"""
NOVAS Star Altitude Calculator - Working Version
Uses the correct NOVAS API functions
"""

from datetime import datetime
import novas.compat as novas

def get_star_altitude(star_name, lat, lon, height=0.0):
    """
    Calculate star altitude using NOVAS
    
    Args:
        star_name: Name of star (e.g., "Vega", "Arcturus", "Sirius")
        lat: Observer latitude (degrees)
        lon: Observer longitude (degrees) 
        datetime_utc: UTC datetime object
        height: Observer height above sea level (meters)
    
    Returns:
        dict: {'altitude': altitude_degrees, 'azimuth': azimuth_degrees}
    """

    # Get star catalog data
    star_catalog = get_navigation_stars()

    star_data = star_catalog[star_name.lower()]
    datetime_utc = star_data["time"]
    # Convert datetime to Julian Date
    jd_utc = novas.julian_date(datetime_utc.year, datetime_utc.month, 
                               datetime_utc.day, datetime_utc.hour + 
                               datetime_utc.minute/60.0 + datetime_utc.second/3600.0)

    # Get delta-T (approximate TT - UTC for 2025)
    #delta_t = 69.0  # seconds
    delta_t = 69.2
    jd_tt = jd_utc + delta_t / 86400.0

    # Create observer location
    location = novas.make_on_surface(lat, lon, height, 10.0, 1013.25)

    if star_name.lower() not in star_catalog:
        raise ValueError(f"Star {star_name} not found in catalog")
    
    # Create star catalog entry using make_cat_entry
    star = novas.make_cat_entry(
        star_data['name'],              # star name
        'HIP',                          # catalog designation
        star_data['catalog_number'],    # catalog number
        star_data['ra'],                # RA in hours
        star_data['dec'],               # Dec in degrees  
        star_data['pm_ra'],             # PM in RA (mas/year)
        star_data['pm_dec'],            # PM in Dec (mas/year)
        star_data['parallax'],          # Parallax (mas)
        star_data['radial_velocity']    # RV (km/s)
    )
    
    # Calculate topocentric star position
    ra_topo, dec_topo = novas.topo_star(jd_tt, 0.0, star, location)
    
    # Convert equatorial to horizontal coordinates
    # Correct call with proper parameters and unpacking
    result = novas.equ2hor(
        jd_ut1=jd_utc,      # Julian date UT1
        delta_t=delta_t,    # TT - UT1 in seconds
        xp=0.0,             # Polar motion x-component (arcsec)
        yp=0.0,             # Polar motion y-component (arcsec)
        location=location,  # Observer location
        ra=ra_topo,         # Right ascension (hours)
        dec=dec_topo,       # Declination (degrees)
        ref_option=1,       # Refraction option (0=no refraction, 1=standard refraction)
        accuracy=0          # Accuracy mode (0=full accuracy, 1=reduced accuracy)
    )
    
    # Unpack the result tuple
    (zd, az), (_, _) = result
    
    # Convert zenith distance to altitude
    altitude = 90.0 - zd
    azimuth = az
    
    return {
        'altitude': altitude,
        'azimuth': azimuth,
        'ra_apparent': ra_topo,
        'dec_apparent': dec_topo,
        'zenith_distance': zd,
        'jd_utc': jd_utc,
        'jd_tt': jd_tt,
        'time' : datetime_utc
    }

def get_navigation_stars():
    """
    Navigation star catalog data 
    J2000.0 epoch coordinates from Hipparcos catalog
    """
    return {
        'vega': {
            'name': 'Vega',
            'catalog_number': 91262,    # Hipparcos number
            'ra': 18.615649,            # Hours (J2000.0)
            'dec': 38.783689,           # Degrees (J2000.0)  
            'pm_ra': 200.94,            # mas/year
            'pm_dec': 287.47,           # mas/year
            'parallax': 128.93,         # mas
            'radial_velocity': -20.60,  # km/s
            'time': datetime(2025, 4, 18, 23, 44, 43)
        },
        'arcturus': {
            'name': 'Arcturus',
            'catalog_number': 69673,    # Hipparcos number
            'ra': 14.261077,            # Hours (J2000.0)
            'dec': 19.182409,           # Degrees (J2000.0)
            'pm_ra': -1093.45,          # mas/year  
            'pm_dec': -1999.40,         # mas/year
            'parallax': 88.83,          # mas
            'radial_velocity': -5.19,   # km/s
            'time': datetime(2025, 4, 18, 23, 48, 46)            
        },
        #'sirius': {
        #    'name': 'Sirius',
        #    'catalog_number': 32349,    # Hipparcos number
        #    'ra': 6.752482,             # Hours (J2000.0)
        #    'dec': -16.716109,          # Degrees (J2000.0)
        #    'pm_ra': -546.01,           # mas/year
        #    'pm_dec': -1223.08,         # mas/year
        #    'parallax': 379.21,         # mas
        #    'radial_velocity': 7.6,     # km/s
        #    'time': datetime(2025, 4, 18, 23, 44, 43)            
        #},
        'capella': {
            'name': 'Capella',
            'catalog_number': 24608,    # Hipparcos number
            'ra': 5.278155,             # Hours (J2000.0)
            'dec': 45.997991,           # Degrees (J2000.0)
            'pm_ra': 75.52,             # mas/year
            'pm_dec': -427.13,          # mas/year
            'parallax': 77.29,          # mas
            'radial_velocity': 30.2,    # km/s
            'time': datetime(2025, 4, 18, 23, 53, 54)            
        }
    }

def compare_with_your_almanac(star_name, lat, lon):
    """
    Helper function to format results for comparison with your almanac
    """
    result = get_star_altitude(star_name, lat, lon)
    
    if result:
        print(f"\n=== NOVAS Results for {star_name.title()} ===")
        print(f"Location: {lat:.6f}°N, {lon:.6f}°E")
        print(f"Time: {result['time']}")
        dms = degrees_to_dms (result["altitude"])
        print(f"Altitude: {result['altitude']:.4f}° ({result['altitude']*60:.1f}')")
        dms = degrees_to_dms (result["altitude"])
        print(f"Altitude (DMS): {dms}")       
        print(f"Azimuth: {result['azimuth']:.4f}°")
        print(f"Apparent RA: {result['ra_apparent']:.6f}h")
        print(f"Apparent Dec: {result['dec_apparent']:.6f}°")
        print(f"Zenith Distance: {result['zenith_distance']:.4f}°")
        
        # Calculate SHA for comparison with nautical almanacs
        # SHA = GHA_Aries - RA (approximately)
        # For exact comparison you'd need GHA Aries at the same time
        print(f"\nFor nautical almanac comparison:")
        print(f"RA (decimal hours): {result['ra_apparent']:.6f}")
        print(f"RA (h m s): {hours_to_hms(result['ra_apparent'])}")
        print(f"Dec (degrees): {result['dec_apparent']:.6f}")
        print(f"Dec (d m s): {degrees_to_dms(result['dec_apparent'])}")
        
        return result
    else:
        print(f"Failed to calculate position for {star_name}")
        return None

def hours_to_hms(decimal_hours):
    """Convert decimal hours to hours:minutes:seconds"""
    h = int(decimal_hours)
    m = int((decimal_hours - h) * 60)
    s = ((decimal_hours - h) * 60 - m) * 60
    return f"{h:02d}h {m:02d}m {s:05.2f}s"

def degrees_to_dms(decimal_degrees):
    """Convert decimal degrees to degrees:minutes:seconds"""
    sign = "+" if decimal_degrees >= 0 else "-"
    decimal_degrees = abs(decimal_degrees)
    d = int(decimal_degrees)
    m = int((decimal_degrees - d) * 60)
    s = ((decimal_degrees - d) * 60 - m) * 60
    return f"{sign}{d:02d}° {m:02d}' {s:05.2f}\""

# Example usage
if __name__ == "__main__":
    # Your test case
    lat = 59.44395460197247
    lon = 19.501688357663202
    
    print("NOVAS Star Altitude Calculator")
    print("=" * 50)
    
    # Test your problematic stars
    test_stars = ['vega', 'arcturus', 'capella']
    
    for star in test_stars:
        #try:
        result = compare_with_your_almanac(star, lat, lon)
        #except Exception as e:
        #    print(f"Error calculating {star}: {e}")
    
    print("\n" + "=" * 50)
    print("Compare these values with your Skyfield almanac and EZ Nautical Almanac!")