''' A toolkit for celestial navigation, in particular sight reductions 
    © August Linnman, 2024, email: august@linnman.net
    MIT License (see LICENSE file)
'''

from math import pi, sin, cos, acos, sqrt, tan, atan2
from datetime import datetime, timezone
from urllib.parse import quote_plus

# Dimension of Earth

EARTH_CIRCUMFERENCE_EQUATORIAL = 40075.017
EARTH_CIRCUMFERENCE_MERIDIONAL = 40007.86
EARTH_CIRCUMFERENCE = (EARTH_CIRCUMFERENCE_EQUATORIAL + EARTH_CIRCUMFERENCE_MERIDIONAL) / 2
EARTH_RADIUS = EARTH_CIRCUMFERENCE / (2 * pi)

# Data types

class LatLon:
    ''' Represents spherical coordinates on Earth '''
    def __init__ (self, lat : float | int, lon : float | int):
        self.lat = lat
        self.lon = mod_lon(lon)

    def __str__(self):
        return "LAT = " + str(self.lat) + "; LON = " + str(self.lon)

    def get_tuple (self) -> tuple[float | int] :
        ''' Used to simplify some code where tuples are more practical '''
        return self.lon, self.lat

# Utility routines (algrebraic, spheric geometry)

def add_vecs (vec1 : list, vec2 : list) -> list:
    ''' Performs addition of two cartesian vectors '''
    assert len (vec1) == len (vec2)
    retval = []
    for i, v in enumerate(vec1):
        retval.append (v + vec2[i])
    return retval

def subtract_vecs (vec1 : list, vec2 : list) -> list:
    ''' Performs subtraction of two cartesian vectors '''
    assert len (vec1) == len (vec2)
    return add_vecs (vec1, mult_scalar_vect(-1, vec2))

def mult_scalar_vect (scalar : int | float, vec : list) -> list:
    ''' Performs multiplication of a cartesian vector with a scalar '''
    retval = []
    for v in vec:
        retval.append (scalar*v)
    return retval

def length_of_vect (vec : list) -> float:
    ''' Returns the absolute value (length) of a vector '''
    s = 0
    for v in vec:
        s += v*v
    return sqrt (s)

def normalize_vect (vec : list) -> list:
    ''' Computes |vec| '''
    len_v = length_of_vect (vec)
    assert len_v > 0
    return mult_scalar_vect (1/len_v, vec)

def cross_product (vec1 : list, vec2 : list) -> list:
    ''' Computes vec1 x vec2 (cross product) '''
    assert len (vec1) == len (vec2) == 3
    retval = [0, 0, 0]
    retval [0] = vec1 [1]*vec2[2] - vec1[2]*vec2[1]
    retval [1] = vec1 [2]*vec2[0] - vec1[0]*vec2[2]
    retval [2] = vec1 [0]*vec2[1] - vec1[1]*vec2[0]
    return retval

def dot_product (vec1 : list, vec2 : list) -> float:
    ''' Computes vec1 * vec2 (dot product) '''
    assert len (vec1) == len (vec2)
    s = 0.0
    for i, v1 in enumerate (vec1):
        s += v1*vec2[i]
    return s

def mod_lon (lon : int | float):
    ''' Transforms a longitude value to the range (-180,180) '''
    x = lon + 180
    x = x % 360
    x = x - 180
    return x

def deg_to_rad (deg : int | float) -> float:
    ''' Convert degrees to radians '''
    return deg/(180.0/pi)

def rad_to_deg (rad : int | float) -> float:
    ''' Convert radians to degrees '''
    return rad*(180.0/pi)

def to_latlon (vec : list) -> LatLon:
    ''' Convert cartesian coordinate to LatLon (spherical) '''
    assert len (vec) == 3
    vec = normalize_vect (vec)

    theta = atan2 (vec[1],vec[0])
    phi = acos (vec[2])
    lon = rad_to_deg (theta)
    lat = 90-rad_to_deg (phi)

    return LatLon (lat, mod_lon(lon))

def to_rectangular (latlon : LatLon) -> list:
    ''' Convert LatLon (spherical) coordinate to cartesian '''
    phi = deg_to_rad (90 - latlon.lat)
    theta = deg_to_rad (latlon.lon)
    a_vec = []
    a_vec.append (cos (theta) * sin (phi))
    a_vec.append (sin (theta) * sin (phi))
    a_vec.append (cos (phi))
    a_vec = normalize_vect (a_vec)
    return a_vec

def get_dms (angle : int | float) -> tuple[int | float]:
    ''' Convert an angle (in degrees) to a tuple of degrees, arc minutes and arc seconds '''
    degrees = int (angle)
    minutes = int ((angle-degrees)*60)
    seconds = (angle-degrees-minutes/60)*3600
    return degrees, minutes, seconds

def get_decimal_degrees (degrees : int | float, minutes : int | float, seconds : int | float)\
      -> float:
    ''' Return decimal value for an angle (from degrees+minutes+seconds) '''
    if degrees < 0:
        minutes = -minutes
        seconds = -seconds
    return degrees + minutes/60 + seconds/3600

def get_decimal_degrees_from_tuple (t : tuple) -> float:
    ''' Return decimal value for an angle, represented as a tuple (degrees, minutes, seconds)'''
    return get_decimal_degrees (t[0], t[1], t[2])

def rotate_vector (vec : list, rot_vec : list, angle_radians : int | float) -> list:
    '''
    Rotate a vector around a rotation vector. Based on Rodrigues formula. 
    https://en.wikipedia.org/wiki/Rodrigues%27_formula
    '''
    assert len(vec) == len(rot_vec) == 3

    v1 = mult_scalar_vect (cos(angle_radians), vec)
    v2 = mult_scalar_vect (sin(angle_radians), cross_product(rot_vec, vec))
    v3 = mult_scalar_vect (dot_product(rot_vec,vec)*(1-cos(angle_radians)), rot_vec)
    result = add_vecs (v1, add_vecs(v2, v3))
    return result

# Course management

def mod_course (lon : int | float) -> float:
    ''' Transform a course angle into the compass range of (0,360) '''
    x = lon % 360
    return x

def takeout_course (latlon : LatLon, course : int | float, speed_knots : int | float,\
                    time_hours : int | float) -> LatLon:
    ''' Calculates a trip movement. Simplified formula, not using great circles '''
    distance = speed_knots * time_hours
    distance_degrees = distance / 60
    # The "stretch" is just taking care of narrowing longitudes on higher latitudes
    stretch_at_start = cos (deg_to_rad (latlon.lat))
    diff_lat = cos (deg_to_rad(course))*distance_degrees
    diff_lon = sin (deg_to_rad(course))*distance_degrees/stretch_at_start
    return LatLon (latlon.lat+diff_lat, latlon.lon+diff_lon)

def angle_b_points (latlon1 : LatLon, latlon2 : LatLon) -> float:
    ''' Calculates the angle between two points on Earth '''
    normvec1 = to_rectangular (latlon1)
    normvec2 = to_rectangular (latlon2)
    dp = dot_product (normvec1, normvec2)
    angle = acos (dp)
    return angle

def distance_between_points (latlon1 : LatLon, latlon2 : LatLon) -> float:
    ''' Calculate distance between two points in km. Using great circles '''
    angle = angle_b_points (latlon1, latlon2)
    distance = EARTH_RADIUS * angle
    return distance

def km_to_nm (km : int | float) -> float:
    ''' Convert from kilometers to nautical miles '''
    return (km / EARTH_CIRCUMFERENCE)*360*60

def nm_to_km (nm : int | float) -> float:
    ''' Convert from nautical miles to kilometers '''
    return (nm/(360*60))*EARTH_CIRCUMFERENCE

# Sextant calibration

class Sextant:
    ''' This class represents a physical sextant, with various errors '''
    def __init__  (self, graduation_error : float):
        self.graduation_error = graduation_error

def angle_between_points (origin : LatLon, point1 : LatLon, point2 : LatLon) -> float:
    ''' Return the angle in degrees between two terrestrial targets (point1 and point2) 
        as seen from the observation point (origin) '''
    origin_r = to_rectangular (origin)
    point_1r = to_rectangular (point1)
    point_2r = to_rectangular (point2)

    point_1gc = normalize_vect (cross_product (origin_r, point_1r))
    point_2gc = normalize_vect (cross_product (origin_r, point_2r))
    dp = dot_product (point_1gc, point_2gc)
    return acos (dp) * (180 / pi)

# Horizon

def get_dip_of_horizon (hm : int | float, temperature : float, dt_dh : float, pressure : float)\
      -> float:
    ''' Calculate dip of horizon in arc minutes 
    Parameter:
        hm : height in meters
    '''
    k_factor = 503*(pressure*10)*(1/((temperature+273)**2))*(0.0343 + dt_dh)
    h = hm / 1000
    r = EARTH_RADIUS
    rr = r / (1 - k_factor)
    the_dip = (acos (rr/(rr+h)))*(180/pi)*60
    return the_dip

def get_intersections (latlon1 : LatLon, latlon2 : LatLon,\
                       angle1 : int | float, angle2 : int | float,\
                       estimated_position : LatLon = None, use_fitness : bool = True)\
                          -> tuple[LatLon | tuple[LatLon], float]:
    '''
    Get intersection of two circles on a spheric surface. 
    At least one of the circles must be a small circle. 
https://math.stackexchange.com/questions/4510171/how-to-find-the-intersection-of-two-circles-on-a-sphere 
    '''
    assert angle1 >= 0 and angle2 >= 0
    assert angle1 < 90 or angle2 < 90  # Make sure one of the circles is a small circle
    # Get cartesian vectors a and b (from ground points)
    a_vec = to_rectangular (latlon1)
    b_vec = to_rectangular (latlon2)

    # Calculate axb
    ab_cross = cross_product (a_vec, b_vec)
    ab_cross = normalize_vect (ab_cross)

    # These steps calculate q which is located halfway between our two intersections
    p1 = mult_scalar_vect (cos(deg_to_rad(angle2)), a_vec)
    p2 = mult_scalar_vect (-cos(deg_to_rad(angle1)), b_vec)
    p3 = add_vecs (p1, p2)
    p3 = normalize_vect (p3)
    p4 = cross_product (ab_cross, p3)
    q = normalize_vect (p4)

    # Calculate a rotation angle
    try:
        if angle1 < angle2:
            rho = acos (cos (deg_to_rad(angle1)) / (dot_product (a_vec, q)))
        else:
            rho = acos (cos (deg_to_rad(angle2)) / (dot_product (b_vec, q)))
    except ValueError as exc:
        raise ValueError ("Bad sight data. Circles do not intersect.") from exc

    # Calculate a rotation vector
    rot_axis = normalize_vect(cross_product (cross_product (a_vec, b_vec), q))

    # Calculate the two intersections by performing rotation of rho and -rho
    int1 = normalize_vect(rotate_vector (q, rot_axis, rho))
    int2 = normalize_vect(rotate_vector (q, rot_axis, -rho))

    # Calculate fitness of intersections.
    fitness = 1
    if use_fitness:
        d1 = add_vecs (int1, mult_scalar_vect(-1,a_vec))
        tang1 = cross_product (d1, a_vec)
        tang1 = normalize_vect (tang1)
        d2 = add_vecs (int1, mult_scalar_vect(-1,b_vec))
        tang2 = cross_product (d2, b_vec)
        tang2 = normalize_vect (tang2)
        weighted = cross_product (tang1, tang2)
        fitness = length_of_vect (weighted)

    ret_tuple = (to_latlon(int1), to_latlon(int2))
    if estimated_position is None:
        return ret_tuple, fitness

    # Check which of the intersections is closest to our estimatedCoordinates
    best_distance = EARTH_CIRCUMFERENCE
    best_intersection = None
    for ints in ret_tuple:
        the_distance = distance_between_points (ints, estimated_position)
        if the_distance < best_distance:
            best_distance = the_distance
            best_intersection = ints
    assert best_intersection is not None
    return best_intersection, fitness

# Atmospheric refraction

def get_refraction (apparent_angle : int | float, temperature : float, pressure : float) -> float:
    '''
    Calculate an estimation of the effect of atmospheric refraction using Bennett's formula
    See: https://en.wikipedia.org/wiki/Atmospheric_refraction#Calculating_refraction 
    
    Parameter:
        apparent_angle: The apparent (measured) altitude in degrees
    Returns:
        The refraction in arc minutes
    '''
    q = pi/180
    h = apparent_angle
    d = h + 7.31 / (h + 4.4)
    d2 = d*q
    return (1 / tan (d2))*(pressure / 101.1)*(283.0/(273.0 + temperature))

# Data formatting

def get_google_map_string (intersections : tuple | LatLon, num_decimals : int) -> str :
    ''' Return a coordinate which can be used in Google Maps '''
    if isinstance (intersections, LatLon):
        return str(round(intersections.lat,num_decimals)) + "," +\
               str(round(intersections.lon,num_decimals))
    elif isinstance (intersections, tuple):
        assert len (intersections) == 2
        return get_google_map_string (intersections[0], num_decimals) + ";" + \
               get_google_map_string (intersections[1], num_decimals)

def get_representation (ins : LatLon | tuple | list, num_decimals : int, lat=False) -> str:
    ''' Converts coordinate(s) to a string representation '''
    assert num_decimals >= 0
    if isinstance (ins, LatLon):
        ins = ins.get_tuple ()
    if isinstance (ins, (float, int)):
        degrees = int (ins)
        if lat:
            if ins < 0:
                prefix = "S"
            else:
                prefix = "N"
        else:
            if ins < 0:
                prefix = "W"
            else:
                prefix = "E"
        minutes = float (abs((ins - degrees)*60))
        a_degrees = abs (degrees)
        return prefix + " " + str(a_degrees) + "°," + str(round(minutes, num_decimals)) + "′"
    if isinstance (ins, (tuple, list)):
        pair = isinstance (ins, tuple)
        length = len (ins)
        ret_val = "("
        for i in range (length-1, -1, -1):
            lat = False
            if pair and i == length-1:
                lat = True
            ret_val = ret_val + get_representation (ins[i], num_decimals, lat)
            if i > 0:
                ret_val = ret_val + ";"
        ret_val = ret_val + ")"
        return ret_val
    raise ValueError ("Incorrect types for represenation.")

# Terrestrial Navigation

def get_circle_for_angle (point1 : LatLon, point2 : LatLon, angle : int | float)\
      -> tuple [LatLon, float] :
    '''
    Calculate the circumscribed circle for two observed points with a specified angle, 
    giving a circle to use for determining terrestrial position 
    '''
    point1_v = to_rectangular (point1)
    point2_v = to_rectangular (point2)

    mid_point = normalize_vect (mult_scalar_vect (1/2, add_vecs (point1_v, point2_v)))
    # Use the basic formula for finding a circumscribing circle
    a = distance_between_points (point1, point2)
    b = (a/2) * (1 / tan (deg_to_rad (angle / 2)))
    c = (a/4) * (1 / (sin (deg_to_rad (angle / 2)) *\
                      cos (deg_to_rad (angle / 2))))
    x = b - c
    # calculate position and radius of circle
    rotation_angle = x / EARTH_RADIUS
    rot_center = rotate_vector (mid_point,\
                               normalize_vect(subtract_vecs (point2_v, point1_v)), rotation_angle)
    radius = rad_to_deg(angle_b_points (to_latlon(rot_center), point1))
    return to_latlon(rot_center), radius

def get_terrestrial_position (point_a1 : LatLon,\
                              point_a2 : LatLon,\
                              angle_a : int | float,\
                              point_b1 : LatLon,\
                              point_b2 : LatLon,\
                              angle_b : int | float,
                              estimated_position : LatLon = None)\
                                  -> tuple [LatLon | tuple, LatLon, float, LatLon, float, float] :
    '''
    Given two pairs of terrestial observations (pos + angle) determine the observer's position 
    '''
    a = get_circle_for_angle (point_a1, point_a2, angle_a)
    b = get_circle_for_angle (point_b1, point_b2, angle_b)
    # Finally compute the intersection.
    # Since we require an estimated position we will eliminate the false intersection.
    intersection, fitness = get_intersections (a[0], b[0], a[1], b[1], estimated_position)
    return intersection, a[0], a[1], b[0], b[1], fitness

# Celestial Navigation

class Sight :
    '''  Object representing a sight (star fix) '''
    def __init__ (self, \
                  object_name : str, \
                  time_year : int, \
                  time_month : int, \
                  time_day : int, \
                  time_hour : int, \
                  time_minute : int, \
                  gha_time_0_degrees : int, \
                  gha_time_0_minutes : int | float, \
                  gha_time_1_degrees : int, \
                  gha_time_1_minutes : int | float, \
                  decl_time_0_degrees : int, \
                  decl_time_0_minutes : int | float, \
                  measured_alt_degrees : int | float, \
                  time_second : int = 0, \
                  measured_alt_minutes : int | float = 0, \
                  measured_alt_seconds : int | float = 0, \
                  decl_time_1_degrees : int = None, \
                  decl_time_1_minutes : int | float = None, \
                  sha_diff_degrees : int | float = 0, \
                  sha_diff_minutes : int | float = 0, \
                  observer_height : int | float = 0, \
                  artificial_horizon : bool = False, \
                  index_error_minutes : int = 0, \
                  semi_diameter_correction : int | float = 0,\
                  horizontal_parallax : int | float = 0,\
                  sextant : Sextant = None,\
                  temperature : float = 10.0,\
                  dt_dh : float = -0.01,\
                  pressure : float = 101.0,
                  ho_obs : bool = False):
        self.temperature          = temperature
        self.dt_dh                = dt_dh
        self.pressure             = pressure
        self.object_name          = object_name
        self.time_year            = time_year
        self.time_month           = time_month
        if self.time_month > 12 or self.time_month < 1:
            raise ValueError ("Month must be within [1,12]")
        self.time_day             = time_day
        if self.time_day > 31 or self.time_day < 1:
            raise ValueError ("Day must be within [0,31]")
        self.time_hour            = time_hour
        if self.time_hour > 23 or self.time_hour < 0:
            raise ValueError ("Hour must be within [0,23]")
        self.time_minute          = time_minute
        if self.time_minute > 59 or self.time_minute < 0:
            raise ValueError ("Minute must be within [0,59]")
        self.time_second          = time_second
        if self.time_second > 59 or self.time_second < 0:
            raise ValueError ("Second must be within [0,59]")
        self.gha_time_0           = get_decimal_degrees\
              (gha_time_0_degrees, gha_time_0_minutes, 0)
        self.gha_time_1           = get_decimal_degrees\
              (gha_time_1_degrees, gha_time_1_minutes, 0)
        if self.gha_time_1 < self.gha_time_0:
            self.gha_time_1 += 360
        if decl_time_1_degrees is None:
            decl_time_1_degrees = decl_time_0_degrees
        if decl_time_1_minutes is None:
            decl_time_1_minutes = decl_time_0_minutes

        self.decl_time_0          = get_decimal_degrees\
              (decl_time_0_degrees, decl_time_0_minutes, 0)
        self.decl_time_1          = get_decimal_degrees\
              (decl_time_1_degrees, decl_time_1_minutes, 0)
        if self.decl_time_0 < -90 or self.decl_time_0 > 90 or \
           self.decl_time_1 < -90 or self.decl_time_1 > 90:
            raise ValueError ("Declination values must be within [-90,90]")
        self.measured_alt         = get_decimal_degrees\
              (measured_alt_degrees, measured_alt_minutes, measured_alt_seconds)
        if self.measured_alt < 0 or self.measured_alt > 90:
            raise ValueError ("Altitude value must be within [0,90]")
        self.sha_diff             = get_decimal_degrees\
              (sha_diff_degrees, sha_diff_minutes, 0)
        self.observer_height      = observer_height
        '''
        if not (self.object_name != "Sun" or self.sha_diff == 0): 
            raise ValueError ("The Sun should have a sha_diff parameter != 0") 
        '''
        if self.observer_height != 0 and artificial_horizon is True:
            raise ValueError ("Observer_height should be == 0 when artificial_horizon == True")
        if self.observer_height < 0:
            raise ValueError ("Observer_height should be >= 0")
        if sextant is not None:
            self.__correct_for_graduation_error (sextant)
        if index_error_minutes != 0:
            self.__correct_for_index_error (index_error_minutes)
        if artificial_horizon:
            self.__correct_for_artficial_horizon ()
        if semi_diameter_correction != 0:
            self.__correct_semi_diameter (semi_diameter_correction)
        if horizontal_parallax != 0:
            self.__correct_for_horizontal_parallax (horizontal_parallax)
        if not ho_obs:
            self.__correct_for_refraction ()
            self.__correct_dip_of_horizon ()
        self.gp = self.__calculate_gp ()

    def __correct_for_graduation_error (self, sextant : Sextant):
        self.measured_alt /= sextant.graduation_error

    def __correct_semi_diameter (self, sd : int | float):
        self.measured_alt += sd/60

    def __correct_for_horizontal_parallax (self, hp : int | float):
        self.measured_alt += hp/60 * sin(deg_to_rad(90 - self.measured_alt))

    def __correct_for_index_error (self, ie : int | float):
        self.measured_alt -= ie/60

    def __correct_for_artficial_horizon (self):
        self.measured_alt /= 2

    def __correct_dip_of_horizon (self):
        if self.observer_height == 0:
            return
        self.measured_alt += get_dip_of_horizon (self.observer_height, self.temperature,\
                                                 self.dt_dh, self.pressure)/60

    def __correct_for_refraction (self):
        self.measured_alt -= get_refraction (self.measured_alt, self.temperature, self.pressure)/60

    def __calculate_gp (self) -> LatLon:

        min_sec_contribution = self.time_minute/60 + self.time_second/3600

        result_lon = mod_lon (- \
        ((self.gha_time_0 + self.sha_diff) + \
        ((self.gha_time_1 - self.gha_time_0))*min_sec_contribution))

        result_lat = \
        self.decl_time_0 + (self.decl_time_1 - self.decl_time_0)*min_sec_contribution

        return LatLon (result_lat, result_lon)

    def get_map_developers_string (self) -> str:
        '''
        Return URL segment for https://mapdevelopers.com circle plotting service
        '''
        result = "["
        result = result + str (round(self.get_radius ()*1000)) + ","
        result = result + str(round(self.gp.lat,4)) + ","
        result = result + str(round(self.gp.lon,4)) + ","
        result = result + "\"#AAAAAA\",\"#000000\",0.4]"
        return result

    def get_angle (self) -> float:
        ''' Returns the (Earth-based) angle of the sight '''
        return 90-self.measured_alt

    def get_radius (self) -> float:
        ''' Returns the radius of the sight (in kilometers) '''
        return (self.get_angle()/360)*EARTH_CIRCUMFERENCE

    def get_distance_from (self, p : LatLon) -> float:
        ''' Return the distance from point (p) to the sight circle of equal altitude '''
        p_distance = distance_between_points (p, self.gp)
        the_radius = self.get_radius ()
        return p_distance - the_radius

class SightPair:
    ''' Represents a pair of sights, needed for making a sight reduction '''
    def __init__ (self, sf1 : Sight, sf2 : Sight):
        self.sf1 = sf1
        self.sf2 = sf2

    def get_intersections (self, estimated_position : LatLon = None) -> tuple[tuple[LatLon], float]:
        ''' Return the two intersections for this sight pair. 
            The parameter estimated_position can be used to eliminate the false intersection '''
        return get_intersections (self.sf1.gp,\
                                  self.sf2.gp,\
                                  self.sf1.get_angle(), self.sf2.get_angle(),\
                                  estimated_position)

class SightCollection:
    ''' Represents a collection of >= 2 sights '''

    def __init__ (self, sf_list : list[Sight]):
        if len (sf_list) < 2:
            raise ValueError ("SightCollection should have at least two sights")
        self.sf_list = sf_list

    def get_intersections (self, limit : int | float = 100, estimated_position = None)\
        -> tuple[tuple[LatLon] | LatLon, float]:
        ''' Get an intersection from the collection of sights. 
            A mean value and sorting algorithm is applied. '''
        nr_of_fixes = len(self.sf_list)
        assert nr_of_fixes >= 2
        if nr_of_fixes == 2:
            # For two star fixes just use the algorithm of SightPair.getIntersections
            intersections = SightPair (self.sf_list[0],\
                                       self.sf_list[1]).get_intersections(estimated_position)
            return intersections
        elif nr_of_fixes >= 3:
            # For >= 3 star fixes perform pairwise calculation on every pair of fixes
            # and then run a sorting algorithm
            coords = list[tuple[LatLon, float]]()
            # Perform pairwise sight reductions
            for i in range (nr_of_fixes):
                for j in range (i+1, nr_of_fixes):
                    p = SightPair (self.sf_list [i], self.sf_list [j])
                    p_int, fitness = p.get_intersections (estimated_position)
                    if p_int is not None:
                        if isinstance (p_int, tuple) or isinstance (p_int, list):
                            #for k in range (len(p_int)):
                            #    coords.append (p_int[k])
                            for pix in p_int:
                                coords.append ((pix, fitness))
                        elif isinstance (p_int, LatLon):
                            coords.append ((p_int, fitness))
                        else:
                            assert False
            nr_of_coords = len (coords)
            dists = dict ()
            # Collect all distance values between intersections
            for i in range (nr_of_coords):
                for j in range (i, nr_of_coords):
                    if i != j:
                        dist = distance_between_points (coords[i][0], coords[j][0])
                        dists [i,j] = dist
            # Sort the distances, with lower distances first
            sorted_dists = dict(sorted(dists.items(), key=lambda item: item[1]))
            # nrOfSortedDists = len (sortedDists)
            chosen_points = set ()
            cp_limit = int((nr_of_fixes**2 - nr_of_fixes) / 2)
            # Find the points which are located close to other points
            for sd in sorted_dists:
                the_distance = sorted_dists [sd]
                if the_distance < limit:
                    chosen_points.add (sd[0])
                    chosen_points.add (sd[1])
                else:
                    break
                if len (chosen_points) > cp_limit:
                    break

            nr_of_chosen_points = len (chosen_points)
            if nr_of_chosen_points == 0:
                # No points found. Bad star fixes. Throw exception.
                raise ValueError ("Bad sight data.")

            # Make sure the chosen points are nearby each other
            #print ("BEST COORDINATES")
            fine_sorting = False # This code is disabled for now
            if fine_sorting:
                for cp1 in chosen_points:
                    print (get_representation (coords[0][cp1],1))
                    for cp2 in chosen_points:
                        if cp1 != cp2:
                            dist = distance_between_points (coords[0][cp1], coords[0][cp2])
                            if dist > limit:
                                # Probably multiple possible observation points.
                                # Best option is to perform sight reduction on 2 sights
                                # and select the correct point manually.
                                raise ValueError\
                                ("Cannot sort multiple intersections to find"+\
                                 "a reasonable set of coordinates")
            #print ("MEAN VALUE COORDINATE from multi-point sight data.")
            #print ("Nr of chosen intersections = " + str(len(chosen_points)))
            summation_vec = [0,0,0]
            # Make a mean value on the best intersections.
            fitness_sum = 0
            for cp in chosen_points:
                selected_coord = coords [cp][0]
                fitness_here   = coords [cp][1]
                fitness_sum += fitness_here
                rect_vec = to_rectangular (selected_coord)
                summation_vec =\
                  add_vecs (summation_vec,\
                  mult_scalar_vect ((1/nr_of_chosen_points)*fitness_here, rect_vec))
            summation_vec = normalize_vect (summation_vec)
            return to_latlon (summation_vec), fitness

    def get_map_developers_string (self) -> str:
        '''
        Return URL for https://mapdevelopers.com circle plotting service
        '''
        url_start = "https://www.mapdevelopers.com/draw-circle-tool.php?circles="
        result = "["
        nr_of_fixes = len(self.sf_list)
        for i in range(nr_of_fixes):
            result = result + self.sf_list [i].get_map_developers_string()
            if i < nr_of_fixes-1:
                result = result + ","
        result = result+"]"
        result = quote_plus (result)
        return url_start + result

class SightTrip:
    ''' Object used for dead-reckoning. Sights are taken on different times
        Course and speed are estimated input parameters.  '''
    def __init__ (self, \
                       sight_start : Sight,\
                       sight_end : Sight,\
                       estimated_starting_point : LatLon,\
                       course_degrees : int | float,\
                       speed_knots : int | float):
        self.sight_start              = sight_start
        self.sight_end                = sight_end
        self.estimated_starting_point = estimated_starting_point
        self.course_degrees           = course_degrees
        self.speed_knots              = speed_knots
        self.__calculate_time_hours ()

    def __calculate_time_hours (self):
        dt1 = datetime(self.sight_start.time_year,\
                       self.sight_start.time_month,\
                       self.sight_start.time_day,\
                       self.sight_start.time_hour,\
                       self.sight_start.time_minute,\
                       self.sight_start.time_second,\
                       tzinfo=timezone.utc)
        it1 = int(dt1.timestamp())
        dt2 = datetime(self.sight_end.time_year,\
                       self.sight_end.time_month,\
                       self.sight_end.time_day,\
                       self.sight_end.time_hour,\
                       self.sight_end.time_minute,\
                       self.sight_end.time_second,\
                       tzinfo=timezone.utc)
        it2 = int(dt2.timestamp())
        self.time_hours = (it2 - it1) / 3600

    def __calculate_distance_to_target (self, angle : int | float, a_vec : list, b_vec : list)\
          -> tuple [float, LatLon, LatLon]:
        rotation_angle = deg_to_rad (angle)
        rotated_vec = rotate_vector (b_vec, a_vec, rotation_angle)
        rotated_latlon = to_latlon (rotated_vec)
        taken_out = takeout_course (rotated_latlon, self.course_degrees,\
                                   self.speed_knots, self.time_hours)

        dbp = distance_between_points (taken_out, self.sight_end.gp) - self.sight_end.get_radius()
        return dbp, taken_out, rotated_latlon

    def get_intersections (self) -> tuple[tuple[LatLon, LatLon], float]:
        ''' Get the intersections for this sight trip object '''
        # Calculate intersections
        pair = SightPair (self.sight_start, self.sight_end)
        best_intersection, fitness = pair.get_intersections\
              (estimated_position = self.estimated_starting_point)

        # Determine angle of the intersection point on sightStart small circle
        a_vec = to_rectangular (self.sight_start.gp)
        b_vec = to_rectangular (best_intersection)
        assert isinstance (best_intersection, LatLon)

        # Apply Newtons method to find the location
        current_rotation = 0
        delta = 0.0001
        limit = 0.001
        iter_limit = 100
        iter_count = 0
        # ready = False
        taken_out = None
        rotated  = None
        while iter_count < iter_limit:
            distance_result, taken_out, rotated =\
                  self.__calculate_distance_to_target (current_rotation, a_vec, b_vec)
            if abs (distance_result) < limit:
                break
            distance_result2, taken_out, rotated =\
                  self.__calculate_distance_to_target (current_rotation+delta, a_vec, b_vec)
            derivative = (distance_result2 - distance_result) / delta
            current_rotation = current_rotation - (distance_result)/derivative
            iter_count += 1
        if iter_count >= iter_limit:
            raise ValueError ("Cannot calculate a trip vector")
        else:
            return (taken_out, rotated), fitness

    def get_map_developers_string (self) -> str:
        '''
        Return URL for https://mapdevelopers.com circle plotting service
        '''
        s_c = SightCollection ([self.sight_start, self.sight_end])
        return s_c.get_map_developers_string ()
