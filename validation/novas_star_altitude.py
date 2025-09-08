"""
NOVAS Star Altitude Calculator - Working Version
Uses the correct NOVAS API functions
"""

from datetime import datetime
import novas.compat as novas

def get_star_altitude(star_name, lat, lon, time, height=0.0):
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
    datetime_utc = time # star_data["time"]
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
    Complete navigation star catalog data
    J2000.0 epoch coordinates from Hipparcos catalog
    All 57 standard navigational stars used in celestial navigation
    """
    return {
        # Northern Stars (High Declination)
        'polaris': {
            'name': 'Polaris',
            'catalog_number': 11767,
            'ra': 2.530301,
            'dec': 89.264109,
            'pm_ra': 44.22,
            'pm_dec': -11.85,
            'parallax': 7.56,
            'radial_velocity': -17.4,
        },
        'kochab': {
            'name': 'Kochab',
            'catalog_number': 85670,
            'ra': 14.845100,
            'dec': 74.155504,
            'pm_ra': -32.29,
            'pm_dec': 11.42,
            'parallax': 26.74,
            'radial_velocity': 16.96,
        },
        'dubhe': {
            'name': 'Dubhe',
            'catalog_number': 54061,
            'ra': 11.062158,
            'dec': 61.751033,
            'pm_ra': -134.11,
            'pm_dec': -34.70,
            'parallax': 26.54,
            'radial_velocity': -9.0,
        },
        'alkaid': {
            'name': 'Alkaid',
            'catalog_number': 67301,
            'ra': 13.792514,
            'dec': 49.313267,
            'pm_ra': -121.23,
            'pm_dec': -15.56,
            'parallax': 31.38,
            'radial_velocity': -10.9,
        },
        'capella': {
            'name': 'Capella',
            'catalog_number': 24608,
            'ra': 5.278155,
            'dec': 45.997991,
            'pm_ra': 75.52,
            'pm_dec': -427.13,
            'parallax': 77.29,
            'radial_velocity': 30.2,
        },
        'vega': {
            'name': 'Vega',
            'catalog_number': 91262,
            'ra': 18.615649,
            'dec': 38.783689,
            'pm_ra': 200.94,
            'pm_dec': 287.47,
            'parallax': 128.93,
            'radial_velocity': -20.60,
        },
        'deneb': {
            'name': 'Deneb',
            'catalog_number': 102098,
            'ra': 20.690531,
            'dec': 45.280339,
            'pm_ra': 1.56,
            'pm_dec': 1.55,
            'parallax': 2.31,
            'radial_velocity': -4.5,
        },
        'altair': {
            'name': 'Altair',
            'catalog_number': 97649,
            'ra': 19.846229,
            'dec': 8.868321,
            'pm_ra': 536.23,
            'pm_dec': 385.29,
            'parallax': 194.95,
            'radial_velocity': -26.1,
        },
        'eltanin': {
            'name': 'Eltanin',
            'catalog_number': 87833,
            'ra': 17.943425,
            'dec': 51.488896,
            'pm_ra': -8.48,
            'pm_dec': -22.79,
            'parallax': 21.14,
            'radial_velocity': -28.07,
        },
        'enif': {
            'name': 'Enif',
            'catalog_number': 107315,
            'ra': 21.736441,
            'dec': 9.875009,
            'pm_ra': 26.92,
            'pm_dec': -0.44,
            'parallax': 4.73,
            'radial_velocity': -5.0,
        },
        'scheat': {
            'name': 'Scheat',
            'catalog_number': 113881,
            'ra': 23.062833,
            'dec': 28.082785,
            'pm_ra': 187.65,
            'pm_dec': 136.93,
            'parallax': 16.37,
            'radial_velocity': -9.1,
        },
        'markab': {
            'name': 'Markab',
            'catalog_number': 113963,
            'ra': 23.079343,
            'dec': 15.205267,
            'pm_ra': 61.1,
            'pm_dec': -42.56,
            'parallax': 23.22,
            'radial_velocity': -4.2,
        },
        
        # Mid-Northern Stars
        'arcturus': {
            'name': 'Arcturus',
            'catalog_number': 69673,
            'ra': 14.261077,
            'dec': 19.182409,
            'pm_ra': -1093.45,
            'pm_dec': -1999.40,
            'parallax': 88.83,
            'radial_velocity': -5.19,
        },
        'spica': {
            'name': 'Spica',
            'catalog_number': 65474,
            'ra': 13.420280,
            'dec': -11.161319,
            'pm_ra': -42.35,
            'pm_dec': -31.73,
            'parallax': 12.44,
            'radial_velocity': 1.0,
        },
        'regulus': {
            'name': 'Regulus',
            'catalog_number': 49669,
            'ra': 10.139509,
            'dec': 11.967208,
            'pm_ra': -248.73,
            'pm_dec': 5.59,
            'parallax': 41.13,
            'radial_velocity': 5.9,
        },
        'alphecca': {
            'name': 'Alphecca',
            'catalog_number': 76267,
            'ra': 15.578106,
            'dec': 26.714693,
            'pm_ra': 120.27,
            'pm_dec': -89.58,
            'parallax': 43.65,
            'radial_velocity': 1.7,
        },
        'rasalhague': {
            'name': 'Rasalhague',
            'catalog_number': 86032,
            'ra': 17.582175,
            'dec': 12.560035,
            'pm_ra': 110.08,
            'pm_dec': -222.61,
            'parallax': 67.13,
            'radial_velocity': -77.4,
        },
        'nunki': {
            'name': 'Nunki',
            'catalog_number': 92855,
            'ra': 18.921068,
            'dec': -26.296724,
            'pm_ra': 12.93,
            'pm_dec': -52.65,
            'parallax': 14.32,
            'radial_velocity': -11.2,
        },
        'antares': {
            'name': 'Antares',
            'catalog_number': 80763,
            'ra': 16.490134,
            'dec': -26.432003,
            'pm_ra': -10.16,
            'pm_dec': -23.30,
            'parallax': 5.40,
            'radial_velocity': -3.4,
        },
        'shaula': {
            'name': 'Shaula',
            'catalog_number': 85927,
            'ra': 17.560115,
            'dec': -37.103824,
            'pm_ra': -8.1,
            'pm_dec': -29.95,
            'parallax': 8.80,
            'radial_velocity': -3.0,
        },
        'sabik': {
            'name': 'Sabik',
            'catalog_number': 84012,
            'ra': 17.173988,
            'dec': -15.724907,
            'pm_ra': 41.16,
            'pm_dec': 97.65,
            'parallax': 37.67,
            'radial_velocity': -0.2,
        },
        'kaus_aust': {
            'name': 'Kaus Aust.',
            'catalog_number': 90185,
            'ra': 18.402695,
            'dec': -34.384616,
            'pm_ra': -39.42,
            'pm_dec': -124.20,
            'parallax': 23.52,
            'radial_velocity': -16.0,
        },
        
        # Equatorial and Tropical Stars
        'aldebaran': {
            'name': 'Aldebaran',
            'catalog_number': 21421,
            'ra': 4.598676,
            'dec': 16.509302,
            'pm_ra': 62.78,
            'pm_dec': -189.36,
            'parallax': 50.09,
            'radial_velocity': 54.3,
        },
        'betelgeuse': {
            'name': 'Betelgeuse',
            'catalog_number': 27989,
            'ra': 5.919529,
            'dec': 7.407064,
            'pm_ra': 27.33,
            'pm_dec': 10.86,
            'parallax': 4.51,
            'radial_velocity': 21.0,
        },
        'bellatrix': {
            'name': 'Bellatrix',
            'catalog_number': 25336,
            'ra': 5.418814,
            'dec': 6.349703,
            'pm_ra': -8.75,
            'pm_dec': -12.88,
            'parallax': 12.92,
            'radial_velocity': 18.2,
        },
        'elnath': {
            'name': 'Elnath',
            'catalog_number': 25428,
            'ra': 5.438199,
            'dec': 28.607452,
            'pm_ra': 23.28,
            'pm_dec': -174.22,
            'parallax': 25.94,
            'radial_velocity': 9.2,
        },
        'alnilam': {
            'name': 'Alnilam',
            'catalog_number': 26311,
            'ra': 5.603563,
            'dec': -1.201919,
            'pm_ra': 1.49,
            'pm_dec': -1.06,
            'parallax': 1.65,
            'radial_velocity': 25.9,
        },
        'rigel': {
            'name': 'Rigel',
            'catalog_number': 24436,
            'ra': 5.242298,
            'dec': -8.201638,
            'pm_ra': 1.31,
            'pm_dec': 0.50,
            'parallax': 3.78,
            'radial_velocity': 17.8,
        },
        'sirius': {
            'name': 'Sirius',
            'catalog_number': 32349,
            'ra': 6.752482,
            'dec': -16.716109,
            'pm_ra': -546.01,
            'pm_dec': -1223.08,
            'parallax': 379.21,
            'radial_velocity': 7.6,
        },
        'procyon': {
            'name': 'Procyon',
            'catalog_number': 37279,
            'ra': 7.654858,
            'dec': 5.224981,
            'pm_ra': -714.590,
            'pm_dec': -1036.80,
            'parallax': 284.56,
            'radial_velocity': -3.2,
        },
        'pollux': {
            'name': 'Pollux',
            'catalog_number': 37826,
            'ra': 7.756422,
            'dec': 28.026199,
            'pm_ra': -625.69,
            'pm_dec': -45.95,
            'parallax': 96.54,
            'radial_velocity': 3.3,
        },
        'alphard': {
            'name': 'Alphard',
            'catalog_number': 46390,
            'ra': 9.459725,
            'dec': -8.658602,
            'pm_ra': -14.49,
            'pm_dec': 33.25,
            'parallax': 18.40,
            'radial_velocity': -4.3,
        },
        'denebola': {
            'name': 'Denebola',
            'catalog_number': 57632,
            'ra': 11.817615,
            'dec': 14.572058,
            'pm_ra': -499.02,
            'pm_dec': -113.78,
            'parallax': 90.16,
            'radial_velocity': -0.1,
        },
        'gienah': {
            'name': 'Gienah',
            'catalog_number': 59803,
            'ra': 12.263422,
            'dec': -17.541929,
            'pm_ra': -159.58,
            'pm_dec': 22.31,
            'parallax': 20.70,
            'radial_velocity': 4.2,
        },
        'alioth': {
            'name': 'Alioth',
            'catalog_number': 62956,
            'ra': 12.900472,
            'dec': 55.959823,
            'pm_ra': 111.74,
            'pm_dec': -8.24,
            'parallax': 39.51,
            'radial_velocity': -9.3,
        },
        'zubenubi': {
            'name': "Zuben'ubi",
            'catalog_number': 72622,
            'ra': 14.847971,
            'dec': -16.041777,
            'pm_ra': -105.69,
            'pm_dec': -69.00,
            'parallax': 43.03,
            'radial_velocity': -35.8,
        },
        
        # Southern Hemisphere Stars (Critical for Southern Ocean navigation)
        'canopus': {
            'name': 'Canopus',
            'catalog_number': 30438,
            'ra': 6.399194,
            'dec': -52.695661,
            'pm_ra': 19.93,
            'pm_dec': 23.24,
            'parallax': 10.43,
            'radial_velocity': 20.5,
        },
        'adhara': {
            'name': 'Adhara',
            'catalog_number': 33579,
            'ra': 6.977127,
            'dec': -28.972084,
            'pm_ra': 2.63,
            'pm_dec': 2.29,
            'parallax': 7.57,
            'radial_velocity': 27.3,
        },
        'suhail': {
            'name': 'Suhail',
            'catalog_number': 44816,
            'ra': 9.133026,
            'dec': -43.432589,
            'pm_ra': -25.52,
            'pm_dec': 13.69,
            'parallax': 11.13,
            'radial_velocity': 18.0,
        },
        'miaplacidus': {
            'name': 'Miaplacidus',
            'catalog_number': 45238,
            'ra': 9.219803,
            'dec': -69.717208,
            'pm_ra': -157.66,
            'pm_dec': 108.91,
            'parallax': 24.51,
            'radial_velocity': -3.5,
        },
        'avior': {
            'name': 'Avior',
            'catalog_number': 41037,
            'ra': 8.375217,
            'dec': -59.509484,
            'pm_ra': -25.34,
            'pm_dec': 22.72,
            'parallax': 4.39,
            'radial_velocity': 21.0,
        },
        'acrux': {
            'name': 'Acrux',
            'catalog_number': 60718,
            'ra': 12.443333,
            'dec': -63.099093,
            'pm_ra': -35.37,
            'pm_dec': -14.73,
            'parallax': 10.17,
            'radial_velocity': -11.2,
        },
        'gacrux': {
            'name': 'Gacrux',
            'catalog_number': 61084,
            'ra': 12.519238,
            'dec': -57.113213,
            'pm_ra': 27.94,
            'pm_dec': -264.33,
            'parallax': 37.09,
            'radial_velocity': 21.4,
        },
        'hadar': {
            'name': 'Hadar',
            'catalog_number': 68702,
            'ra': 14.063763,
            'dec': -60.373035,
            'pm_ra': -33.96,
            'pm_dec': -25.06,
            'parallax': 7.63,
            'radial_velocity': -12.0,
        },
        'rigil_kent': {
            'name': 'Rigil Kent.',
            'catalog_number': 71683,
            'ra': 14.660617,
            'dec': -60.835389,
            'pm_ra': -3678.19,
            'pm_dec': 481.84,
            'parallax': 747.23,
            'radial_velocity': -25.1,
        },
        'menkent': {
            'name': 'Menkent',
            'catalog_number': 68933,
            'ra': 14.111168,
            'dec': -36.369958,
            'pm_ra': -519.29,
            'pm_dec': -517.87,
            'parallax': 88.83,
            'radial_velocity': -5.0,
        },
        'atria': {
            'name': 'Atria',
            'catalog_number': 82273,
            'ra': 16.811045,
            'dec': -69.027710,
            'pm_ra': 17.85,
            'pm_dec': -32.92,
            'parallax': 7.85,
            'radial_velocity': -3.2,
        },
        'peacock': {
            'name': 'Peacock',
            'catalog_number': 100751,
            'ra': 20.427294,
            'dec': -56.735090,
            'pm_ra': 7.71,
            'pm_dec': -86.15,
            'parallax': 17.99,
            'radial_velocity': 1.2,
        },
        'al_nair': {
            'name': "Al Na'ir",
            'catalog_number': 109268,
            'ra': 22.137216,
            'dec': -46.960974,
            'pm_ra': 127.60,
            'pm_dec': -147.91,
            'parallax': 31.39,
            'radial_velocity': -7.6,
        },
        'fomalhaut': {
            'name': 'Fomalhaut',
            'catalog_number': 113368,
            'ra': 22.960833,
            'dec': -29.622237,
            'pm_ra': 329.22,
            'pm_dec': -164.22,
            'parallax': 129.81,
            'radial_velocity': 6.5,
        },
        
        # Circumpolar and Arctic Stars
        'alpheratz': {
            'name': 'Alpheratz',
            'catalog_number': 677,
            'ra': 0.139793,
            'dec': 29.090431,
            'pm_ra': 135.68,
            'pm_dec': -162.95,
            'parallax': 33.62,
            'radial_velocity': -10.7,
        },
        'schedar': {
            'name': 'Schedar',
            'catalog_number': 3179,
            'ra': 0.675075,
            'dec': 56.537331,
            'pm_ra': 50.36,
            'pm_dec': -32.17,
            'parallax': 14.27,
            'radial_velocity': -4.3,
        },
        'ankaa': {
            'name': 'Ankaa',
            'catalog_number': 2081,
            'ra': 0.438077,
            'dec': -42.306084,
            'pm_ra': 232.76,
            'pm_dec': -353.62,
            'parallax': 42.11,
            'radial_velocity': 74.6,
        },
        'diphda': {
            'name': 'Diphda',
            'catalog_number': 3419,
            'ra': 0.726339,
            'dec': -17.986606,
            'pm_ra': 232.55,
            'pm_dec': 31.99,
            'parallax': 33.86,
            'radial_velocity': -13.8,
        },
        'achernar': {
            'name': 'Achernar',
            'catalog_number': 7588,
            'ra': 1.628556,
            'dec': -57.236753,
            'pm_ra': 87.00,
            'pm_dec': -40.35,
            'parallax': 22.68,
            'radial_velocity': 16.0,
        },
        'hamal': {
            'name': 'Hamal',
            'catalog_number': 9884,
            'ra': 2.119563,
            'dec': 23.462418,
            'pm_ra': 188.55,
            'pm_dec': -145.77,
            'parallax': 49.56,
            'radial_velocity': 14.2,
        },
        'acamar': {
            'name': 'Acamar',
            'catalog_number': 13847,
            'ra': 2.971073,
            'dec': -40.304672,
            'pm_ra': 87.00,
            'pm_dec': -88.62,
            'parallax': 23.39,
            'radial_velocity': 17.0,
        },
        'menkar': {
            'name': 'Menkar',
            'catalog_number': 14135,
            'ra': 3.038040,
            'dec': 4.089737,
            'pm_ra': -11.81,
            'pm_dec': -78.76,
            'parallax': 14.82,
            'radial_velocity': 26.1,
        },
        'mirfak': {
            'name': 'Mirfak',
            'catalog_number': 15863,
            'ra': 3.405376,
            'dec': 49.861179,
            'pm_ra': 24.11,
            'pm_dec': -26.01,
            'parallax': 6.44,
            'radial_velocity': -2.04,
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