''' A toolkit for celestial navigation, in particular sight reductions 
    © August Linnman, 2024, email: august@linnman.net
    MIT License (see LICENSE file)
'''

from math import  pi, sin, cos, acos, sqrt, tan, atan2
from datetime import datetime
from urllib.parse import quote_plus
# import logging
from types import NoneType

# Dimension of Earth

EARTH_CIRCUMFERENCE_EQUATORIAL = 40075.017
EARTH_CIRCUMFERENCE_MERIDIONAL = 40007.86
EARTH_CIRCUMFERENCE = (EARTH_CIRCUMFERENCE_EQUATORIAL + EARTH_CIRCUMFERENCE_MERIDIONAL) / 2
EARTH_RADIUS = EARTH_CIRCUMFERENCE / (2 * pi)


EARTH_RADIUS_GEODETIC_EQUATORIAL = 6378
EARTH_RADIUS_GEODETIC_POLAR      = 6357
EARTH_FLATTENING =\
    (EARTH_RADIUS_GEODETIC_EQUATORIAL - EARTH_RADIUS_GEODETIC_POLAR) / \
     EARTH_RADIUS_GEODETIC_EQUATORIAL

# Data types

class LatLon:
    ''' Represents spherical coordinates on Earth '''
    def __init__ (self, lat : float | int, lon : float | int):
        self.lat = lat
        self.lon = mod_lon(lon)

    def __str__(self):
        return "LAT = " + str(round(self.lat,4)) + "; LON = " + str(round(self.lon,4))

    def get_tuple (self) -> tuple[float | int, float | int] :
        ''' Used to simplify some code where tuples are more practical '''
        return self.lon, self.lat

# Utility routines (algrebraic, spheric geometry)

def add_vecs (vec1 : list[float], vec2 : list[float]) -> list[float]:
    ''' Performs addition of two cartesian vectors '''
    assert len (vec1) == len (vec2)
    retval = list [float] ()
    for i, v in enumerate(vec1):
        retval.append (v + vec2[i])
    return retval

def subtract_vecs (vec1 : list[float], vec2 : list[float]) -> list [float]:
    ''' Performs subtraction of two cartesian vectors '''
    assert len (vec1) == len (vec2)
    return add_vecs (vec1, mult_scalar_vect(-1, vec2))

def mult_scalar_vect (scalar : int | float, vec : list [float]) -> list [float]:
    ''' Performs multiplication of a cartesian vector with a scalar '''
    retval = list [float] ()
    for v in vec:
        retval.append (scalar*v)
    return retval

def length_of_vect (vec : list [float]) -> float:
    ''' Returns the absolute value (length) of a vector '''
    s = 0
    for v in vec:
        s += v*v
    return sqrt (s)

def normalize_vect (vec : list [float]) -> list [float]:
    ''' Computes |vec| '''
    len_v = length_of_vect (vec)
    assert len_v > 0
    return mult_scalar_vect (1/len_v, vec)

def cross_product (vec1 : list [float], vec2 : list [float]) -> list [float]:
    ''' Computes vec1 x vec2 (cross product) '''
    assert len (vec1) == len (vec2) == 3
    retval = [0.0, 0.0, 0.0]
    retval [0] = vec1 [1]*vec2[2] - vec1[2]*vec2[1]
    retval [1] = vec1 [2]*vec2[0] - vec1[0]*vec2[2]
    retval [2] = vec1 [0]*vec2[1] - vec1[1]*vec2[0]
    return retval

def dot_product (vec1 : list [float], vec2 : list [float]) -> float:
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

def to_latlon (vec : list [float]) -> LatLon:
    ''' Convert cartesian coordinate to LatLon (spherical) '''
    assert len (vec) == 3
    vec = normalize_vect (vec)

    theta = atan2 (vec[1],vec[0])
    phi = acos (vec[2])
    lon = rad_to_deg (theta)
    lat = 90-rad_to_deg (phi)

    return LatLon (lat, mod_lon(lon))

def to_rectangular (latlon : LatLon) -> list [float]:
    ''' Convert LatLon (spherical) coordinate to cartesian '''
    phi = deg_to_rad (90 - latlon.lat)
    theta = deg_to_rad (latlon.lon)
    a_vec = list [float] ()
    a_vec.append (cos (theta) * sin (phi))
    a_vec.append (sin (theta) * sin (phi))
    a_vec.append (cos (phi))
    a_vec = normalize_vect (a_vec)
    return a_vec

def get_dms (angle : int | float) -> tuple[int, int, int | float]:
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

def rotate_vector\
    (vec : list [float], rot_vec : list [float], angle_radians : int | float) -> list [float]:
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

def takeout_course (latlon : LatLon, course : int | float, speed_knots : int | float,
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
    ''' Calculates the angle between two points on Earth 
        Return : Angle in radians '''
    normvec1 = to_rectangular (latlon1)
    normvec2 = to_rectangular (latlon2)
    dp = dot_product (normvec1, normvec2)
    angle = acos (dp)
    return angle

def spherical_distance (latlon1 : LatLon, latlon2 : LatLon) -> float:
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

#pylint: disable=R0903
class Sextant:
    ''' This class represents a physical sextant, with various errors '''
    def __init__  (self,
                   graduation_error : float = 1.0,
                   index_error : int | float = 0):
        """ Parameters
                graduation_error : ratio between read and actual altitude. (Linear relation)
                                   Use 1.0 for the same values.
                index_error : Error in arcminutes. (Fixed error)
        """
        self.graduation_error = graduation_error
        self.index_error = index_error
#pylint: enable=R0903

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

# Chronometer

class Chronometer: # pylint: disable=R0903
    ''' This class represents a chronometer (clock) with known error/drift '''
    def __init__ (self, set_time : str, set_time_deviation_seconds : int | float,
                  drift_sec_per_day : int | float):
        self.set_time = datetime.fromisoformat(set_time)
        self.set_time_deviation_seconds = set_time_deviation_seconds
        self.drift_sec_per_day = drift_sec_per_day

    def get_corrected_time (self, measured_time : datetime) -> datetime:
        ''' Calculate proper time based on a measured time '''
        st1 = int(self.set_time.timestamp())
        mt1 = int(measured_time.timestamp())
        diff_days = (mt1 - st1) / (24*3600)
        drift = diff_days * self.drift_sec_per_day
        mt_corr = mt1 - drift
        return datetime.fromtimestamp (mt_corr)
# pylint: enable=R0903

# Horizon

def get_adjusted_earth_radius (temperature : float = 10,
                               dt_dh : float = -0.01, pressure : float = 101) -> float:
    ''' Calculate the modified earth radius as a result of refraction 
        Returns : The adjusted radius in km
    '''
    k_factor = 503*(pressure*10)*(1/((temperature+273)**2))*(0.0343 + dt_dh)
    r = EARTH_RADIUS
    return r / (1 - k_factor)

def get_dip_of_horizon (hm : int | float, temperature : float = 10,
                        dt_dh : float = -0.01, pressure : float = 101)\
      -> float:
    ''' Calculate dip of horizon in arc minutes 
    Parameters:
        hm : height in meters
        temperature : temperature in degrees Celsius
        dt_th : temperature gradient in degrees Celsius / meter
    '''
    #k_factor = 503*(pressure*10)*(1/((temperature+273)**2))*(0.0343 + dt_dh)
    #r = EARTH_RADIUS
    #rr = r / (1 - k_factor)
    rr = get_adjusted_earth_radius (temperature, dt_dh, pressure)
    h = hm / 1000
    the_dip = (acos (rr/(rr+h)))*(180/pi)*60
    return the_dip

def get_line_of_sight (h1 : float, h2 : float, temperature : float = 10,
                       dt_dh : float = -0.01, pressure : float = 101) -> float:
    ''' Geometry for line-of-sight '''
    rr = get_adjusted_earth_radius (temperature, dt_dh, pressure) * 1000
    x1a = sqrt (((rr + h1)**2) - rr**2)
    x1r = atan2 (x1a, rr)
    x1 = x1r * rr
    x2a = sqrt (((rr + h2)**2) - rr**2)
    x2r = atan2 (x2a, rr)
    x2 = x2r * rr
    return x1 + x2

# Intersections

#pylint: disable=R0903
class Circle:
    ''' Helper class for circles (great or small circles) '''

    def __init__ (self, latlon : LatLon, angle : int | float, circumference : float):
        ''' Parameters:
                latlon : centerpoint
                angle  : angle of circle in degrees, for a great circle set to 90
        '''
        self.latlon                 = latlon
        self.angle                  = angle
        self.circumference          = circumference
        self.accum_mapping_distance = None
        self.mapping_distance_count = 0

    def make_geodetic (self) :
        ''' TODO '''
        self.latlon = LatLonGeodetic (ll=self.latlon)
        return self

    def __str__(self) -> str:
        return "CIRCLE: LATLON = [" + str(self.latlon) + "]; ANGLE = " + str(round(self.angle,4))

    def accumulate_distance (self, distance : float) :
        ''' Accumulates mapping distances, in order to build a mean value '''
        if self.accum_mapping_distance is None:
            self.accum_mapping_distance = distance
            self.mapping_distance_count = 1
        else:
            self.accum_mapping_distance += distance
            self.mapping_distance_count += 1

    def get_mapping_distance (self) -> float | NoneType:
        ''' Retrieve the mean value of mapping distances '''
        if self.accum_mapping_distance is None:
            return None
        else:
            return self.accum_mapping_distance / self.mapping_distance_count

    def set_mapping_distance (self, distance : float | NoneType = None):
        ''' Insert a new mapping distance estimation '''
        self.accum_mapping_distance = distance
        self.mapping_distance_count = 1

    def get_map_developers_string\
        (self, include_url_start : bool, color : str = "000000") -> str:
        ''' Get MD string for this circle '''
        if include_url_start:
            url_start = MAP_DEV_URL
            result = "["
        else:
            url_start = ""
            result = ""
        result += get_map_developers_string\
              (self.get_radius(), self.latlon, self.get_mapping_distance(), color=color)
        if include_url_start:
            result += "]"
            result = quote_plus (result)
        return url_start + result

    def get_radius (self) -> float:
        ''' Returns the radius of the sight (in kilometers) '''
        return (self.angle/360)*self.circumference

class CircleCollection:
    ''' Simple collection of circles '''
    def __init__ (self, coll : list[Circle]):
        self.c_list = coll

    def make_geodetic (self):
        ''' TODO '''
        for c in self.c_list:
            c.make_geodetic ()

    def get_map_developers_string (self, color : str = "000000") -> str:
        ''' Return the MD string '''
        url_start = MAP_DEV_URL
        result = "["
        clen = len(self.c_list)
        for i in range (clen):
            result += self.c_list[i].get_map_developers_string\
                  (include_url_start=False, color = color)
            if i < clen - 1:
                result += ","
        result += "]"
        result = quote_plus (result)
        return url_start + result

#pylint: enable=R0903

def get_great_circle_route (start : LatLon, direction : LatLon | float | int) -> Circle:
    ''' Calculates a great circle starting in 'start' 
        and passing 'direction' coordinate (if LatLon) 
        or with direction 'direction' degrees (if float or int)    
    '''
#pylint: disable=C0123
    if isinstance (direction, LatLon):
        assert type(start) == type(direction)
#pylint: enable=C0123

    converted = False
    if isinstance (start, LatLonGeodetic):
        start = start.get_latlon()
        converted = True
        if isinstance (direction, LatLonGeodetic):
            direction = direction.get_latlon()

    if isinstance (direction, LatLon):
        t1 = to_rectangular (start)
        t2 = to_rectangular (direction)
        t3 = normalize_vect(cross_product (t1,t2))
        t4 = to_latlon (t3)
        distance_ratio = 1
        distance = EARTH_CIRCUMFERENCE / 4
        if converted:
            t4 = LatLonGeodetic (ll=t4)
            distance = spherical_distance (t4, LatLonGeodetic(ll=start))
            distance_ratio = distance / (EARTH_CIRCUMFERENCE/4)
        c = Circle (t4, 90*distance_ratio, EARTH_CIRCUMFERENCE)
        # c.set_mapping_distance (distance)
        return c
    # isinstance (direction, float) or isinstance (direction, int) == True
    if start.lat in (90,-90):
        raise ValueError ("Cannot take a course from any of the poles")
    north_pole = [0.0, 0.0, 1.0] # to_rectangular (LatLon (90, 0))
    b = to_rectangular (start)
    east_tangent = normalize_vect(cross_product (b, north_pole))
    rotated = rotate_vector (east_tangent, b, deg_to_rad(90 - direction))
    cp = normalize_vect(cross_product (b, rotated))
    cp_latlon = to_latlon (cp)
    distance_ratio = 1
    distance = EARTH_CIRCUMFERENCE / 4
    if converted:
        cp_latlon = LatLonGeodetic (ll = cp_latlon)
        distance = spherical_distance (cp_latlon, LatLonGeodetic(ll=start))
        distance_ratio = distance / (EARTH_CIRCUMFERENCE / 4)
    c = Circle (cp_latlon, 90*distance_ratio, EARTH_CIRCUMFERENCE)
    c.set_mapping_distance (distance)
    return c


class IntersectError (ValueError):
    ''' Exception used for failed intersections '''

    def __init__ (self, info : str):
        super().__init__ (info)

#pylint: disable=R0912
#pylint: disable=R0913
#pylint: disable=R0914
#pylint: disable=R0915
def get_intersections (circle1 : Circle, circle2 : Circle,
                       estimated_position : NoneType | LatLon = None,
                       use_fitness : bool = True, diagnostics : bool = False,
                       intersection_number : int = 0) \
                          -> tuple[
                              LatLon | tuple[LatLon, LatLon], # Coordinate or Coordinate Pair
                              float,                          # Fitness value
                              str]:                           # Diagnostic output
    '''
    Get intersection of two circles on a spheric surface. 
https://math.stackexchange.com/questions/4510171/how-to-find-the-intersection-of-two-circles-on-a-sphere 
    Parameters:
        latlon1 : GP nr 1 location
        latlon2 : GP nr 2 location
        angle1 : Angle from zenith of star fix 1 (in radians)
        angle2 : Angle from zenith of star fix 2 (in radians)
        estimated_position : A DRP position, if available. Set to None if unknown. 
        use_fitness : Set to True if fitness calculation is requested.
        diagnostics : Set to True if diagnostics is required. 
                      Diagnostics is returned as the third item in return value tuple. 
        intersection_number : Used for diagnostics to label output. 

    This algorithm seems to work very well for geocentric data, but not for 
    geodetic (ellipsoidal) data. A general design decision is to make all intersection
    work in the geocentrical system, and convert/transform to/from geodetical when needed. 
    '''
    assert circle1.angle >= 0 and circle2.angle >= 0

    # Handle intersection of two great circles
    if circle1.angle == 90 and circle2.angle == 90:
        a_vec = to_rectangular (circle1.latlon)
        b_vec = to_rectangular (circle2.latlon)
        c1_vec = cross_product (a_vec, b_vec)
        if length_of_vect (c1_vec) == 0:
            raise IntersectError ("GP:s are the same or antipodal (Two great circles)")
        c1_vec_n = normalize_vect (c1_vec)
        c2_vec_n = mult_scalar_vect (-1, c1_vec_n)
        c1_latlon = to_latlon (c1_vec_n)
        c2_latlon = to_latlon (c2_vec_n)
        ret_tuple = (c1_latlon, c2_latlon)
        diag_output = ""
        if diagnostics:
            diag_output = "Handling two great circles with standard cross-product formula"
        fitness = 1
        if use_fitness:
            fitness = length_of_vect (c1_vec)
        if estimated_position is None:
            dist1 = spherical_distance\
                  (LatLonGeodetic(ll=c1_latlon), LatLonGeodetic(ll=circle1.latlon))
            circle1.accumulate_distance (dist1)
            dist2 = spherical_distance\
                  (LatLonGeodetic(ll=c1_latlon), LatLonGeodetic(ll=circle2.latlon))
            circle2.accumulate_distance (dist2)
            dist3 = spherical_distance\
                  (LatLonGeodetic(ll=c2_latlon), LatLonGeodetic(ll=circle1.latlon))
            circle1.accumulate_distance (dist3)
            dist4 = spherical_distance\
                  (LatLonGeodetic(ll=c2_latlon), LatLonGeodetic(ll=circle2.latlon))
            circle2.accumulate_distance (dist4)
            return ret_tuple, fitness, diag_output
        else:
            # Check which of the intersections is closest to our estimatedCoordinates
            best_distance = EARTH_CIRCUMFERENCE
            best_intersection = None
            for ints in ret_tuple:
                the_distance = spherical_distance (ints, estimated_position)
                if the_distance < best_distance:
                    best_distance = the_distance
                    best_intersection = ints
            dist1 = spherical_distance\
                  (LatLonGeodetic(ll=best_intersection), LatLonGeodetic(ll=circle1.latlon))
            circle1.accumulate_distance (dist1)
            dist2 = spherical_distance\
                  (LatLonGeodetic(ll=best_intersection), LatLonGeodetic(ll=circle2.latlon))
            circle2.accumulate_distance (dist2)
            assert best_intersection is not None
            return best_intersection, fitness, diag_output

    # Handle intersection of two circles, of which at least one is a small circle
    diag_output = ""
    # Get cartesian vectors a and b (from ground points)
    if diagnostics:
        if intersection_number != 0:
            diag_output += "\n## Performing an intersection (#"+str(intersection_number)+")\n\n"
        else:
            diag_output += "\n## Performing an intersection\n\n"
        diag_output += "### **Input parameters**\n"
        diag_output +=\
        "$\\textbf{latlon1}=("+str(round(circle1.latlon.lat,4))+","+\
            str(round(circle1.latlon.lon,4))+")$<br/>"
        diag_output +=\
        "$\\textbf{angle1}=("+str(round(circle1.angle,4))+")$<br/>"        
        diag_output +=\
        "$\\textbf{latlon2}=("+str(round(circle2.latlon.lat,4))+","+\
            str(round(circle2.latlon.lon,4))+")$<br/>"
        diag_output +=\
        "$\\textbf{angle2}=("+str(round(circle2.angle,4))+")$<br/>"
        if estimated_position is not None:
            diag_output +=\
            "$\\textbf{EstimatedPosition}=("+\
                str(round(estimated_position.lat,4))+","+\
                str(round(estimated_position.lon,4))+")$<br/>"
    a_vec = to_rectangular (circle1.latlon)
    b_vec = to_rectangular (circle2.latlon)
    if diagnostics:
        diag_output += "\n### **Converting positions to cartesisans**\n"
        diag_output += " * $\\text{latlon1}$ converted to cartesians $=("+\
                         str(round(a_vec[0],4))+","+\
                         str(round(a_vec[1],4))+","+\
                         str(round(a_vec[2],4))+")\\text{ ==> }\\textbf{aVec}$\n"
        diag_output += " * $\\text{latlon2}$ converted to cartesians $=("+\
                         str(round(b_vec[0],4))+","+\
                         str(round(b_vec[1],4))+","+\
                         str(round(b_vec[2],4))+")\\text{ ==> }\\textbf{bVec}$<br/>"
    # Calculate N(axb)
    ab_cross = cross_product (a_vec, b_vec)
    if length_of_vect (ab_cross) == 0:
        raise IntersectError ("Failed to calculate intersection. Identical source points?")
    ab_cross = normalize_vect (ab_cross)
    if diagnostics:
        #diag_output +=\
        #     "$\\text{We compute the normalized cross product of aVec and bVec}$</br>"
        diag_output +=\
        "\n### **We compute the normalized cross product of $\\text{aVec}$ and $\\text{bVec}$**\n"
        diag_output += "* **Definition**: $N$ is vector normalization:"+\
                       " $\\mathit{N(x)=\\frac{x}{|x|}}$\n"
        diag_output += "* $N(\\text{aVec}\\times\\text{bVec})=("+\
                        str(round(ab_cross[0],4))+","+\
                        str(round(ab_cross[1],4))+","+\
                        str(round(ab_cross[2],4))+")\\text{ ==> }\\textbf{abCross}$<br/>"

    # These steps calculate q which is located halfway between our two intersections
    if diagnostics:
        diag_output +=\
        "\n### **Now we compute the vector $\\text{q}$, being at the midpoint between" +\
         " $\\text{aVec}$ and $\\text{bVec}$**\n"
    p1 = mult_scalar_vect (cos(deg_to_rad(circle2.angle)), a_vec)
    if diagnostics:
        diag_output +=\
        "* We compute $\\text{p1}$\n"
        diag_output += "    * $cos(\\text{angle1})\\cdot\\text{aVec} = ("+\
            str(round(p1[0],4))+","+\
            str(round(p1[1],4))+","+\
            str(round(p1[2],4))+")\\text{ ==> }\\textbf{p1}"+\
            "$\n"
    p2 = mult_scalar_vect (-cos(deg_to_rad(circle1.angle)), b_vec)
    if diagnostics:
        diag_output +=\
        "* We compute $\\text{p2}$\n"
        diag_output += "    * $-cos(\\text{angle2})\\cdot\\text{bVec} = ("+\
            str(round(p2[0],4))+","+\
            str(round(p2[1],4))+","+\
            str(round(p2[2],4))+")\\text{ ==> }\\textbf{p2}"+\
            "$\n"    
    p3 = add_vecs (p1, p2)
    if diagnostics:
        diag_output +=\
        "* Perform addition\n"
        diag_output += "    * $\\text{p1}+\\text{p2} = ("+\
            str(round(p3[0],4))+","+\
            str(round(p3[1],4))+","+\
            str(round(p3[2],4))+")\\text{ ==> }\\textbf{p3}"+\
            "$\n"
    p3 = normalize_vect (p3)
    if diagnostics:
        diag_output +=\
        "* Normalize $\\text{p3}$\n"
        diag_output += "    * $N(\\text{p3}) = ("+\
            str(round(p3[0],4))+","+\
            str(round(p3[1],4))+","+\
            str(round(p3[2],4))+")\\text{ ==> }\\textbf{p3}"+\
            "$\n"
    q = cross_product (ab_cross, p3)
    if diagnostics:
        diag_output +=\
        "* Perform cross product and get mid-point\n"
        diag_output += "    * $\\text{abCross}\\times{\\text{p3}} = ("+\
            str(round(q[0],4))+","+\
            str(round(q[1],4))+","+\
            str(round(q[2],4))+")\\text{ ==> }\\textbf{q}"+\
            "$\n"

    # Calculate a rotation angle
    if diagnostics:
        diag_output +=\
        "\n### **Calculating the rotation angle and vector to find the "+\
        "intersections from $\\text{q}$**\n"
    try:
        if circle1.angle < circle2.angle:
            rho = acos (cos (deg_to_rad(circle1.angle)) / (dot_product (a_vec, q)))
            if diagnostics:
                diag_output +=\
                "* $\\arccos{\\left(\\frac {\\cos{\\left(\\text{angle1}\\right)}}"+\
                "{\\text{aVec}\\cdot\\text{q}}\\right)}"
        else:
            rho = acos (cos (deg_to_rad(circle2.angle)) / (dot_product (b_vec, q)))
            if diagnostics:
                diag_output +=\
                "* $\\arccos{\\left(\\frac {\\cos{\\left(\\text{angle2}\\right)}}"+\
                "{\\text{bVec}\\cdot\\text{q}}\\right)}"
        if diagnostics:
            diag_output += "=" + str(round(rho,4)) + "\\text{ ==> }\\rho$ (rotation angle)\n"
    except ValueError as exc:
        raise IntersectError ("Bad sight data. Circles do not intersect.") from exc

    # Calculate a rotation vector
    rot_axis = normalize_vect(cross_product (cross_product (a_vec, b_vec), q))
    if diagnostics:
        diag_output +=\
        "* $N\\left(\\left(\\text{aVec}\\times\\text{bVec}\\right)"+\
        " \\times {\\text{q}} \\right) = ("+\
        str(round(rot_axis[0],4))+","+\
        str(round(rot_axis[1],4))+","+\
        str(round(rot_axis[2],4))+")\\text{ ==> }\\textbf{rotAxis}"+\
        "$\n"

    # Calculate the two intersections by performing rotation of rho and -rho
    if diagnostics:
        diag_output += "* Compute the two intersection points with rotation operations.\n"+\
                       "    * **Definition**: $GR$ is Gauss rotation formula: "+\
                       "$\\mathit{GR(q,r,\\tau) = "+\
                       "q \\cos \\tau + \\left( r \\times q \\right) \\sin \\tau + "+\
                       "r \\left(r \\cdot q \\right)\\left(1 - \\cos \\tau \\right)}$\n"

    int1 = rotate_vector (q, rot_axis, rho)
    if diagnostics:
        diag_output += "    * $GR\\left(\\text{q},\\text{rotAxis},\\rho\\right) = ("+\
        str(round(int1[0],4))+","+\
        str(round(int1[1],4))+","+\
        str(round(int1[2],4))+")\\text{ ==> }\\textbf{int1}"+\
        "$\n"
    int2 = rotate_vector (q, rot_axis, -rho)
    if diagnostics:
        diag_output += "    * $GR\\left(\\text{q},\\text{rotAxis},-\\rho\\right) = ("+\
        str(round(int2[0],4))+","+\
        str(round(int2[1],4))+","+\
        str(round(int2[2],4))+")\\text{ ==> }\\textbf{int2}"+\
        "$\n"

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

    int1_latlon = to_latlon (int1)
    int2_latlon = to_latlon (int2)
    if diagnostics:
        diag_output += "* Converting the intersections to LatLon\n"
        diag_output += "    * $\\text{int1}$ converts to $("+\
        str(round(int1_latlon.lat,4))+","+\
        str(round(int1_latlon.lon,4))+")\\text{ ==> }\\textbf{Intersection 1}$\n"
        diag_output += "    * $\\text{int2}$ converts to $("+\
        str(round(int2_latlon.lat,4))+","+\
        str(round(int2_latlon.lon,4))+")\\text{ ==> }\\textbf{Intersection 2}$\n"
    ret_tuple = (int1_latlon, int2_latlon)

    if estimated_position is None:
        dist1 = spherical_distance\
              (LatLonGeodetic(ll=int1_latlon), LatLonGeodetic(ll=circle1.latlon))
        circle1.accumulate_distance (dist1)
        dist2 = spherical_distance\
              (LatLonGeodetic(ll=int1_latlon), LatLonGeodetic(ll=circle2.latlon))
        circle2.accumulate_distance (dist2)
        dist3 = spherical_distance\
              (LatLonGeodetic(ll=int2_latlon), LatLonGeodetic(ll=circle1.latlon))
        circle1.accumulate_distance (dist3)
        dist4 = spherical_distance\
              (LatLonGeodetic(ll=int2_latlon), LatLonGeodetic(ll=circle2.latlon))
        circle2.accumulate_distance (dist4)
        return ret_tuple, fitness, diag_output
    else:
        # Check which of the intersections is closest to our estimatedCoordinates
        best_distance = EARTH_CIRCUMFERENCE
        best_intersection = None
        for ints in ret_tuple:
            the_distance = spherical_distance (ints, estimated_position)
            if the_distance < best_distance:
                best_distance = the_distance
                best_intersection = ints
        dist1 = spherical_distance\
              (LatLonGeodetic(ll=best_intersection), LatLonGeodetic(ll=circle1.latlon))
        circle1.accumulate_distance (dist1)
        dist2 = spherical_distance\
              (LatLonGeodetic(ll=best_intersection), LatLonGeodetic(ll=circle2.latlon))
        circle2.accumulate_distance (dist2)
        assert best_intersection is not None
        return best_intersection, fitness, diag_output
#pylint: enable=R0912
#pylint: enable=R0913
#pylint: enable=R0914
#pylint: enable=R0915

def get_azimuth (to_pos : LatLon, from_pos : LatLon) -> float:
    ''' Return the azimuth of the to_pos sight from from_pos sight
        Returns the azimuth in degrees (0-360)
        Parameters:
            to_pos : LatLon of the observed position
            from_pos : LatLon of the observing positio
        Returns: 
            The aziumuth angle (degrees 0-360)
    '''
    # From the poles we need to calculate azimuths differently
    if from_pos.lat == 90:
        return (-to_pos.lon) % 360
    if from_pos.lat == -90:
        return to_pos.lon % 360
    # Antipodes has to be handled
    if (to_pos.lat == -from_pos.lat) and (((to_pos.lon - from_pos.lon) % 180) == 0):
        return 0
    # Same coordinate?
    if (to_pos.lat == from_pos.lat) and (to_pos.lon == from_pos.lon):
        return 0

    a = to_rectangular (to_pos)
    b = to_rectangular (from_pos)
    north_pole = [0.0, 0.0, 1.0] # to_rectangular (LatLon (90, 0))
    east_tangent = normalize_vect(cross_product (north_pole, b))
    north_tangent = normalize_vect (cross_product (b, east_tangent))
    direction = normalize_vect(subtract_vecs (a,b))
    fac1 = dot_product (direction, north_tangent)
    fac2 = dot_product (direction, east_tangent)
    r = rad_to_deg (atan2 (fac2, fac1))
    return r % 360

# Time management

def calculate_time_hours (dt1 : datetime, dt2 : datetime):
    '''
    Return the difference between two timestamps in hours
    '''
    it1 = int(dt1.timestamp())
    it2 = int(dt2.timestamp())
    return (it2 - it1) / 3600

# Atmospheric refraction

def get_refraction (apparent_angle : int | float, temperature : float, pressure : float) -> float:
    '''
    Calculate an estimation of the effect of atmospheric refraction using Bennett's formula
    See: https://en.wikipedia.org/wiki/Atmospheric_refraction#Calculating_refraction 
    
        Parameters:
            apparent_angle : The apparent (measured) altitude in degrees.
            temperature : Temperature in degrees celsius.
            pressure : Pressure in kPa.
        Returns:
            The refraction in arc minutes
    '''
    q = pi/180
    h = apparent_angle
    d = h + 7.31 / (h + 4.4)
    d2 = d*q
    retval = (1 / tan (d2))*(pressure / 101.1)*(283.0/(273.0 + temperature))
    return retval

# Data formatting

#pylint: disable=R1710
def get_google_map_string (intersections : tuple | LatLon, num_decimals : int) -> str :
    ''' Return a coordinate which can be used in Google Maps 
    
        Parameters:
            intersections : A data set of intersection points
            num_decimals : Required precision
        Returns: 
            A string usable as a Google Maps coordinate
    '''
    if isinstance (intersections, LatLon):
        type_string = "("+str(type(intersections))+")"
        return type_string + "," +\
               str(round(intersections.lat,num_decimals)) + "," +\
               str(round(intersections.lon,num_decimals))
    if isinstance (intersections, tuple):
        assert len (intersections) == 2
        return get_google_map_string (intersections[0], num_decimals) + ";" + \
               get_google_map_string (intersections[1], num_decimals)
#pylint: enable=R1710

MAP_DEV_URL = "https://www.mapdevelopers.com/draw-circle-tool.php?circles="

def get_map_developers_string\
     (r : float, latlon : LatLon, distance : float | NoneType = None,
      color : str = "000000") -> str:
    '''
    Return URL segment for https://mapdevelopers.com circle plotting service
    '''
    # Compensate for the behaviour in mapdevelopers.com. Circles have to be drawn slightly wider
    scale_factor = 1.00083
    if distance is not None:
        r = distance

    r = r * scale_factor
    result = "["
    result = result + str (round(r*1000)) + ","
    result = result + str(round(latlon.lat,6)) + ","
    result = result + str(round(latlon.lon,6)) + ","
    result = result + "\"#AAAAAA\",\"#"+color+"\",0.4]"
    return result

def get_representation\
    (ins : LatLon | tuple | list [float] | float | int, num_decimals : int,
     lat : bool =False) -> str:
    ''' Converts coordinate(s) to a string representation 
    
        Parameters: 
            ins : A set of coordinates
            lat : True if latitude, False if longitude
        Returns:
            A representation string. 
    '''
    assert num_decimals >= 0
    if isinstance (ins, LatLon):
        ins = ins.get_tuple ()
    if isinstance (ins, (float, int)):
        degrees = int (ins)
        if lat:
            if degrees < 0:
                prefix = "S"
            else:
                prefix = "N"
        else:
            if degrees < 0:
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

def parse_angle_string (angle_string : str) -> float:
    ''' Read a string "DD:MM:SS" and return a decimal degree value.
        Minute and second specifications are optional. 
        Decimal values can be used. 

        Parameters:
            angle_string : A string in the DD[:MM[:SS]]] format.
        Returns
            An angle in decimal degrees. 
    '''
    splitted = angle_string.split (":")
    degrees = minutes = seconds = None
    if len (splitted) == 0 or len (splitted) > 3:
        raise ValueError ("Invalid number of items in angle specification")
    try:
        degrees = float(splitted [0])
        try:
            minutes = float (splitted [1])
            seconds = float (splitted [2])
        except IndexError:
            pass
    except ValueError as exc:
        raise ValueError ("Invalid data in angle specification") from exc
    ret_val = degrees
    if minutes is not None:
        if degrees < 0:
            minutes = -minutes
        ret_val += minutes / 60
    if seconds is not None:
        if degrees < 0:
            seconds = -seconds
        ret_val += seconds / 3600
    return ret_val

# Terrestrial Navigation

def get_circle_for_angle (point1 : LatLon, point2 : LatLon, angle : int | float)\
      -> Circle :
      #-> tuple [LatLon, float] :
    '''
    Calculate the circumscribed circle for two observed points with a specified angle, 
    giving a circle to use for determining terrestrial position 
    '''
    point1_v = to_rectangular (point1)
    point2_v = to_rectangular (point2)

    mid_point = normalize_vect (mult_scalar_vect (1/2, add_vecs (point1_v, point2_v)))
    # Use the basic formula for finding a circumscribing circle
    a = spherical_distance (point1, point2)
    b = (a/2) * (1 / tan (deg_to_rad (angle / 2)))
    c = (a/4) * (1 / (sin (deg_to_rad (angle / 2)) *\
                      cos (deg_to_rad (angle / 2))))
    x = b - c
    # calculate position and radius of circle
    rotation_angle = x / EARTH_RADIUS
    rot_center = rotate_vector (mid_point,\
                               normalize_vect(subtract_vecs (point2_v, point1_v)), rotation_angle)
    radius = rad_to_deg(angle_b_points (to_latlon(rot_center), point1))
    return Circle (to_latlon(rot_center), radius, EARTH_CIRCUMFERENCE)
    #return to_latlon(rot_center), radius

#pylint: disable=R0913
def get_terrestrial_position (point_a1 : LatLon,
                              point_a2 : LatLon,
                              angle_a : int | float,
                              point_b1 : LatLon,
                              point_b2 : LatLon,
                              angle_b : int | float,
                              estimated_position : LatLon | NoneType = None,
                              diagnostics : bool = False)\
            -> tuple [LatLon | tuple, Circle, Circle, float, str] :
    '''
    Given two pairs of terrestial observations (pos + angle) determine the observer's position 
    '''

    a = get_circle_for_angle (point_a1, point_a2, angle_a)
    b = get_circle_for_angle (point_b1, point_b2, angle_b)
    # Finally compute the intersection.
    # Since we require an estimated position we will eliminate the false intersection.
    intersection, fitness, diag_output =\
        get_intersections (a, b, estimated_position=estimated_position,\
                           diagnostics=diagnostics)
    return intersection, a, b, fitness, diag_output
#pylint: enable=R0913

# Geodetics

class LatLonGeodetic (LatLon):
    ''' Represents a geodetic coordinate in an ellipsoid model (WGS-84) '''
    def __init__ (self,
                  lat : float | int | NoneType = None,
                  lon : float | int | NoneType = None,
                  ll : LatLon | NoneType = None):
        if ll is None:
            # Define the coordinate just from raw lat and lon values
            assert lat is not None
            assert lon is not None
            super().__init__ (lat, lon)
            return

        if isinstance (ll, LatLonGeodetic):
            super().__init__ (ll.lat, ll.lon)
            return

        # ll is a *Geocentrical* position
        # Transforms a geocentric coordinate into geodetic
        #    See: https://www.mathworks.com/help/aeroblks/geocentrictogeodeticlatitude.html
        lam_bda = deg_to_rad (ll.lat)
        a       = EARTH_RADIUS_GEODETIC_EQUATORIAL
        b       = EARTH_RADIUS_GEODETIC_POLAR
        f       = EARTH_FLATTENING
        r       = EARTH_RADIUS
        rho     = r * cos(lam_bda)
        z       = r * sin(lam_bda)
        e2      = f*(2-f)
        r       = a
        eprim2  = e2 / (1 - e2)
        iter_ready = False
        iter_count = 0
        iter_limit = 10
        diff_limit = 10**-8
        mu = pi/4
        while not iter_ready:
            beta = atan2 ((1-f)*sin(mu), cos(mu))
            new_mu = atan2 (z + b*eprim2*(sin(beta)**3),\
                            rho-a*e2*((cos(beta)**3)))
            if abs(new_mu - mu) < diff_limit:
                iter_ready = True
            else:
                mu = new_mu
            iter_count += 1
            if iter_count > iter_limit:
                iter_ready = True

        # return LatLonGeodetic (ll.lat, ll.lon)
        #self.lat = rad_to_deg (mu)
        #self.lon = ll.lon
        super().__init__(rad_to_deg(mu), ll.lon)

    def get_latlon (self, height : float = 0) -> LatLon:
        ''' Transforms a geodetic coordinate into geocentric 
            See: https://www.mathworks.com/help/aeroblks/geodetictogeocentriclatitude.html
        '''
        f = EARTH_FLATTENING
        a = EARTH_RADIUS_GEODETIC_EQUATORIAL / (2*pi)
        assert self.lat is not None
        mu = deg_to_rad(self.lat)
        e2 = f*(2-f)
        h = height
        n = a / sqrt(1 - e2*(sin(mu))**2)
        rho = (n + h) * cos(mu)
        z = (n*(1 - e2) + h)*sin(mu)
        lam_bda = atan2 (z, rho)
        assert self.lon is not None
        return LatLon (rad_to_deg(lam_bda), self.lon)

    def __str__(self):
        return "Geodetic coordinate. LAT = " + str(round(self.lat,4)) +\
               "; LON = " + str(round(self.lon,4))


def get_vertical_parallax (llg : LatLonGeodetic) -> tuple [float, LatLon]:
    ''' Calculate the vertical parallax 
    (difference between geocentric and geodetic latitude)
    '''
    ll  = llg.get_latlon ()
    llg_rect = to_rectangular (llg)
    ll_rect  = to_rectangular (ll)
    angle    = dot_product (ll_rect, llg_rect)
    return rad_to_deg(acos (angle)), ll

def get_geocentric_alt (position : LatLonGeodetic, geodesic_alt : float, gp : LatLon) -> float:
    ''' Convert an estimated geodetic altitude (observation from sextant) to a geocentric value '''
    #if False:
    #    parallax, ll = get_vertical_parallax (estimated_position)
    #    est_rect = to_rectangular (estimated_position)
    #    ll_rect  = to_rectangular (ll)
    #    rot_vec = cross_product (est_rect, ll_rect)
    #    gp_rect = to_rectangular (gp)
    #    rotated = normalize_vect(rotate_vector (gp_rect, rot_vec, deg_to_rad(parallax)))
    #    dot_p = dot_product (rotated, ll_rect)
    #    return rad_to_deg((pi/2) - acos(dot_p))
    ang_1 = (pi/2) - acos(dot_product (to_rectangular(position), to_rectangular(gp)))
    epgc = position.get_latlon()
    ang_2 = (pi/2) - acos(dot_product (to_rectangular(epgc),     to_rectangular(gp)))
    diff = rad_to_deg(ang_2 - ang_1)
    return geodesic_alt + diff

def get_geodetic_alt (position : LatLon, geocentric_alt : float, gp : LatLon) -> float:
    ''' Convert an estimated geocentric altitude to a geodetic value '''
    ang_1 = (pi/2) - acos(dot_product (to_rectangular(position), to_rectangular(gp)))
    epgc = LatLonGeodetic(ll = position)
    ang_2 = (pi/2) - acos(dot_product (to_rectangular(epgc),     to_rectangular(gp)))
    diff = rad_to_deg(ang_2 - ang_1)
    return geocentric_alt + diff

#pylint: disable=C0103
#pylint: disable=R0914
def ellipsoidal_distance(pt1 : LatLon, pt2 : LatLon) -> float:
    ''' Compute a distance on an path on an ellipsoid
        From: https://www.johndcook.com/blog/2018/11/24/spheroid-distance/   
    '''

    if not isinstance (pt1, LatLonGeodetic):
        pt1_g = LatLonGeodetic (ll = pt1)
        pt1 = pt1_g
    if not isinstance (pt2, LatLonGeodetic):
        pt2_g = LatLonGeodetic (ll = pt2)
        pt2 = pt2_g

    a = EARTH_RADIUS_GEODETIC_EQUATORIAL # 6378137.0 # equatorial radius in meters
    f = EARTH_FLATTENING # ellipsoid flattening
    b = (1 - f)*a
    tolerance = 1e-11 # to stop iteration

    lat1  = deg_to_rad(pt1.lat)
    long1 = deg_to_rad(pt1.lon)
    lat2  = deg_to_rad(pt2.lat)
    long2 = deg_to_rad(pt2.lon)

    phi1, phi2 = lat1, lat2
    U1 = atan2((1-f)*tan(phi1),1)
    U2 = atan2((1-f)*tan(phi2),1)
    L1, L2 = long1, long2
    L = L2 - L1

    lambda_old = L + 0

    while True:

        t = (cos(U2)*sin(lambda_old))**2
        t += (cos(U1)*sin(U2) - sin(U1)*cos(U2)*cos(lambda_old))**2
        sin_sigma = t**0.5
        cos_sigma = sin(U1)*sin(U2) + cos(U1)*cos(U2)*cos(lambda_old)
        sigma = atan2(sin_sigma, cos_sigma)

        sin_alpha = cos(U1)*cos(U2)*sin(lambda_old) / sin_sigma
        cos_sq_alpha = 1 - sin_alpha**2
        cos_2sigma_m = cos_sigma - 2*sin(U1)*sin(U2)/cos_sq_alpha
        C = f*cos_sq_alpha*(4 + f*(4-3*cos_sq_alpha))/16

        t = sigma + C*sin_sigma*(cos_2sigma_m + C*cos_sigma*(-1 + 2*cos_2sigma_m**2))
        lambda_new = L + (1 - C)*f*sin_alpha*t
        if abs(lambda_new - lambda_old) <= tolerance:
            break
        else:
            lambda_old = lambda_new

    u2 = cos_sq_alpha*((a**2 - b**2)/b**2)
    A = 1 + (u2/16384)*(4096 + u2*(-768+u2*(320 - 175*u2)))
    B = (u2/1024)*(256 + u2*(-128 + u2*(74 - 47*u2)))
    t = cos_2sigma_m + 0.25*B*(cos_sigma*(-1 + 2*cos_2sigma_m**2))
    t -= (B/6)*cos_2sigma_m*(-3 + 4*sin_sigma**2)*(-3 + 4*cos_2sigma_m**2)
    delta_sigma = B * sin_sigma * t
    s = b*A*(sigma - delta_sigma)

    return s
#pylint: enable=R0914
#pylint: enable=C0103

# Celestial Navigation

#pylint: disable=R0902
class Sight :
    '''  Object representing a sight (star fix) '''

    estimated_position_hold = None
#pylint: disable=R0912
#pylint: disable=R0913
#pylint: disable=R0914
    def __init__ (self, \
                  object_name              : str,
                  set_time                 : str,
                  gha_time_0               : str,
                  gha_time_1               : str,
                  decl_time_0              : str,
                  measured_alt             : str,
                  estimated_position       : LatLonGeodetic | NoneType = None,
                  decl_time_1              : NoneType | str = None,
                  sha_diff                 : NoneType | str = None,
                  observer_height          : int | float = 0,
                  artificial_horizon       : bool = False,
                  index_error_minutes      : int | float = 0,
                  semi_diameter_correction : int | float = 0,
                  horizontal_parallax      : int | float = 0,
                  sextant                  : NoneType | Sextant = None,
                  chronometer              : NoneType | Chronometer = None,
                  temperature              : float = 10.0,
                  dt_dh                    : float = -0.01,
                  pressure                 : float = 101.0,
                  ho_obs                   : bool = False,
                  no_dip                   : bool = False):
        self.mapping_distance     = None
        self.temperature          = temperature
        self.dt_dh                = dt_dh
        self.pressure             = pressure
        self.object_name          = object_name
        self.set_time_dt          = datetime.fromisoformat (set_time)
        self.gha_time_0           = parse_angle_string (gha_time_0)
        self.gha_time_1           = parse_angle_string (gha_time_1)
        if self.gha_time_1 < self.gha_time_0:
            self.gha_time_1 += 360
        if decl_time_1 is None:
            decl_time_1 = decl_time_0
        self.decl_time_0          = parse_angle_string (decl_time_0)
        self.decl_time_1          = parse_angle_string (decl_time_1)
        if self.decl_time_0 < -90 or self.decl_time_0 > 90 or \
           self.decl_time_1 < -90 or self.decl_time_1 > 90:
            raise ValueError ("Declination values must be within [-90,90]")
        self.measured_alt         = parse_angle_string (measured_alt)
        if sha_diff is not None:
            self.sha_diff         = parse_angle_string (sha_diff)
        else:
            self.sha_diff         = 0
        self.observer_height      = observer_height
        #if not (self.object_name != "Sun" or self.sha_diff == 0):
        #    raise ValueError ("The Sun should have a sha_diff parameter != 0")
        if self.observer_height != 0 and artificial_horizon is True:
            raise ValueError ("Observer_height should be == 0 when artificial_horizon == True")
        if self.observer_height < 0:
            raise ValueError ("Observer_height should be >= 0")
        if sextant is not None:
            self.__correct_for_error (sextant)
        if chronometer is not None:
            self.__correct_set_time (chronometer)
        if index_error_minutes != 0:
            self.__correct_for_index_error (index_error_minutes)
        if artificial_horizon:
            self.__correct_for_artficial_horizon ()
        if self.measured_alt < 0 or self.measured_alt > 90:
            raise ValueError ("Altitude value must be within [0,90]")
        if semi_diameter_correction != 0:
            self.__correct_semi_diameter (semi_diameter_correction)
        if horizontal_parallax != 0:
            self.__correct_for_horizontal_parallax (horizontal_parallax)
        if not ho_obs:
            self.__correct_for_refraction ()
            if not no_dip:
                self.__correct_dip_of_horizon ()
        self.gp = self.__calculate_gp ()
        if estimated_position is None:
            self.estimated_position = Sight.estimated_position_hold
        else:
            self.estimated_position = estimated_position

        Sight.estimated_position_hold = self.estimated_position
        self.raw_measured_alt = self.measured_alt
        if isinstance (self.estimated_position, LatLonGeodetic):
            # We must convert the sextant altitude (geodetic) to a geocentric value
            self.measured_alt =\
                get_geocentric_alt (self.estimated_position,\
                                    self.measured_alt, self.gp)
        # At this point the altitude values are saved
        # self.measured_alt     = A corrected *geocentrical* altitude
        #      This value is used for all intersection work
        # self.raw_measured_alt = A corrected *geodetical* altitude
        #      This value is used for all mapping work
        # self.gp               = The geographical point in *geocentrical* system
        #      The gp must be converted to geodetical wherever needed.

#pylint: enable=R0912
#pylint: enable=R0913
#pylint: enable=R0914


    def __correct_set_time (self, chronometer : Chronometer):
        dt1 = self.set_time_dt
        dt2 = chronometer.get_corrected_time (dt1)
        self.set_time_dt = dt2

    def __correct_for_error (self, sextant : Sextant):
        self.measured_alt /= sextant.graduation_error
        self.measured_alt -= sextant.index_error/60

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

        min_sec_contribution = self.set_time_dt.minute/60 + self.set_time_dt.second/3600

        result_lon = mod_lon (- \
        ((self.gha_time_0 + self.sha_diff) + \
        ((self.gha_time_1 - self.gha_time_0))*min_sec_contribution))

        result_lat = \
        self.decl_time_0 + (self.decl_time_1 - self.decl_time_0)*min_sec_contribution

        return LatLon (result_lat, result_lon)

    def get_angle (self, geodetic : bool, viewpoint : LatLon| NoneType = None) -> float:
        ''' Returns the (Earth-based) angle of the sight '''
        if geodetic:
            if viewpoint is not None:
                ell_dist = ellipsoidal_distance (viewpoint, LatLonGeodetic (ll=self.gp))
                wp = LatLonGeodetic (lat = viewpoint.lat, lon = viewpoint.lon)
                wplatlon = wp.get_latlon()
                sph_dist = spherical_distance (wplatlon, self.gp)
                return (90-self.raw_measured_alt)*(ell_dist / sph_dist)
            return 90-self.raw_measured_alt

        return 90-self.measured_alt

    def get_circle (self, geodetic : bool, viewpoint : LatLon | NoneType = None) -> Circle:
        ''' Return a circle object corresponding to this Sight '''
        circumference = EARTH_CIRCUMFERENCE
        if geodetic:
            gp_x = LatLonGeodetic (ll = self.gp)
        else:
            gp_x = self.gp
        retval = Circle (gp_x, self.get_angle(geodetic=geodetic,viewpoint=viewpoint),\
                       circumference)
        retval.set_mapping_distance (self.mapping_distance)
        return retval

    def get_distance_from (self, p : LatLon, geodetic : bool) -> float:
        ''' Return the spherical distance from point (p) to the sight circle of equal altitude '''
        p_distance = spherical_distance (p, self.gp)
        the_radius = self.get_circle(geodetic=geodetic).get_radius ()
        return p_distance - the_radius

    def get_azimuth (self, from_pos : LatLon) -> float:
        ''' Return the azimuth of this sight (to the GP) from a particular point on Earth 
            Returns the azimuth in degrees (0-360)'''
        return get_azimuth (self.gp, from_pos)

    def set_mapping_distance (self, distance : float | NoneType) :
        ''' Attach a mapping distance estimation '''
        self.mapping_distance = distance

    def get_map_developers_string (self, include_url_start : bool,
                                   geodetic : bool,
                                   viewpoint : LatLonGeodetic | NoneType = None) -> str:
        '''
        Return URL segment for https://mapdevelopers.com circle plotting service
        '''
        result = self.get_circle(geodetic=geodetic, viewpoint=viewpoint).get_map_developers_string\
            (include_url_start = include_url_start)
        return result
#pylint: enable=R0902

#pylint: disable=R0903
class SightPair:
    ''' Represents a pair of sights, needed for making a sight reduction '''
    def __init__ (self, sf1 : Sight, sf2 : Sight):
        self.sf1 = sf1
        self.sf2 = sf2

    def get_intersections\
                      (self, return_geodetic : bool, estimated_position : NoneType | LatLon = None,
                       diagnostics : bool = False,
                       intersection_number : int = 0) ->\
                       tuple[LatLon | tuple[LatLon, LatLon], float, str]:
        ''' Return the two intersections for this sight pair. 
            The parameter estimated_position can be used to eliminate the false intersection '''

        circle1 = self.sf1.get_circle (geodetic = return_geodetic)
        circle2 = self.sf2.get_circle (geodetic = return_geodetic)
        retval = get_intersections (circle1, circle2,
                                estimated_position=estimated_position,\
                                diagnostics = diagnostics,
                                intersection_number = intersection_number)
        dist1 = circle1.get_mapping_distance ()
        self.sf1.set_mapping_distance (dist1)
        dist2 = circle2.get_mapping_distance ()
        self.sf2.set_mapping_distance (dist2)
        return retval

#pylint: enable=R0903

class SightCollection:
    ''' Represents a collection of >= 2 sights '''

    def __init__ (self, sf_list : list[Sight]):
        if len (sf_list) < 2:
            raise ValueError ("SightCollection should have at least two sights")
        self.sf_list = sf_list

#pylint: disable=R0912
#pylint: disable=R0914
#pylint: disable=R0915
    def get_intersections\
        (self, return_geodetic : bool, limit : int | float = 100,
          estimated_position : NoneType | LatLon = None,
          diagnostics : bool = False) \
            -> tuple[LatLon | tuple[LatLon, LatLon], float, str]:
        ''' Get an intersection from the collection of sights. 
            A mean value and sorting algorithm is applied. '''
        if estimated_position is None:
            estimated_position = Sight.estimated_position_hold
        diag_output = ""
        nr_of_fixes = len(self.sf_list)
        assert nr_of_fixes >= 2
        if nr_of_fixes == 2:
            # For two star fixes just use the algorithm of SightPair.getIntersections
            intersections, fitness, diag_output =\
                   SightPair (self.sf_list[0],\
                              self.sf_list[1]).get_intersections\
                                         (return_geodetic=return_geodetic,
                                          estimated_position=estimated_position,\
                                          diagnostics = diagnostics)
            if return_geodetic:
                if isinstance (intersections, tuple):
                    ret_intersections = LatLonGeodetic (ll=intersections[0]),\
                                        LatLonGeodetic (ll=intersections[1])
                else:
                    ret_intersections = LatLonGeodetic (ll=intersections)
            else:
                ret_intersections = intersections
            return ret_intersections, fitness, diag_output
        #elif nr_of_fixes >= 3:
        # For >= 3 star fixes perform pairwise calculation on every pair of fixes
        # and then run a sorting algorithm
        coords = list[tuple[LatLon, float]]()
        # Perform pairwise sight reductions
        intersection_count = 0
        for i in range (nr_of_fixes):
            for j in range (i+1, nr_of_fixes):
                p = SightPair (self.sf_list [i], self.sf_list [j])
                intersection_count += 1
                p_int, fitness, dia =\
                    p.get_intersections (return_geodetic=return_geodetic,
                                         estimated_position=estimated_position,\
                                         diagnostics = diagnostics,\
                                         intersection_number = intersection_count)
                diag_output += dia
                if p_int is not None:
                    if isinstance (p_int, (list, tuple)):
                        for pix in p_int:
                            coords.append ((pix, fitness))
                    elif isinstance (p_int, LatLon):
                        coords.append ((p_int, fitness))
                    else:
                        assert False
        nr_of_coords = len (coords)
        dists = dict ()
        # Collect all distance values between intersections
        if diagnostics:
            diag_output += "## Distance table\n\n"
            diag_output += "Intersections\n"
            diag_output += "| Id | Coordinate |\n"
            diag_output += "|----|------------|\n"
            for i in range (nr_of_coords):
                diag_output += "|**"+str(i)+"**|"+str(coords[i][0])+"|\n"
            diag_output += "\n\nDistances\n"

        if diagnostics:
            diag_output += "|"
            for i in range (nr_of_coords):
                diag_output += "|" + str(i)
            diag_output += "|\n"
            diag_output += "|----"
            for i in range (nr_of_coords):
                diag_output += "|----"
            diag_output += "|\n"
        for i in range (nr_of_coords):
            diag_output += "|**" + str(i) + "**"
            if diag_output:
                for _ in range (0, i):
                    diag_output += "|-"
            for j in range (i, nr_of_coords):
                if i != j:
                    dist = spherical_distance (coords[i][0], coords[j][0])
                    dists [i,j] = dist
                    if diagnostics:
                        diag_output += "|" + str(round(dist,1)) + " km"
                else:
                    if diagnostics:
                        diag_output += "|/"
            if diagnostics:
                diag_output += "|\n"
        if diagnostics:
            diag_output += "\n\n"
        # Sort the distances, with lower distances first
        sorted_dists = dict(sorted(dists.items(), key=lambda item: item[1]))
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
            raise IntersectError ("Bad sight data.")

        # Make sure the chosen points are nearby each other
        fine_sorting = False # This code is disabled for now
        if fine_sorting:
            for cp1 in chosen_points:
                print (get_representation (coords[0][cp1],1))
                for cp2 in chosen_points:
                    if cp1 != cp2:
                        dist = spherical_distance (coords[0][cp1], coords[0][cp2])
                        if dist > limit:
                            # Probably multiple possible observation points.
                            # Best option is to perform sight reduction on 2 sights
                            # and select the correct point manually.
                            raise IntersectError\
                            ("Cannot sort multiple intersections to find"+\
                                "a reasonable set of coordinates")

        summation_vec = [0.0,0.0,0.0]
        # Make a mean value on the best intersections.
        fitness_sum = 0
        for cp in chosen_points:
            selected_coord = coords [cp][0]
            if return_geodetic:
                selected_coord_x = LatLonGeodetic (ll = selected_coord)
            else:
                selected_coord_x = selected_coord
            fitness_here = coords [cp][1]**3 # Penalize bad intersections
            fitness_sum += fitness_here
            rect_vec = to_rectangular (selected_coord_x)
            summation_vec =\
                add_vecs (summation_vec,\
                mult_scalar_vect ((1/nr_of_chosen_points)*fitness_here, rect_vec))
        summation_vec = normalize_vect (summation_vec)
        return to_latlon (summation_vec), fitness_sum, diag_output
#pylint: enable=R0912
#pylint: enable=R0914
#pylint: enable=R0915

    def get_map_developers_string \
        (self, geodetic : bool, markers : list[LatLonGeodetic] | NoneType = None,
         viewpoint : LatLon | NoneType = None) -> str:
        '''
        Return URL for https://mapdevelopers.com circle plotting service
        '''
        c_l = list [Circle] ()
        for s in self.sf_list:
            a_circle = s.get_circle(geodetic=geodetic, viewpoint=viewpoint)
            c_l.append (a_circle)
        if isinstance (markers, list):
            for m in markers:
                c_l.append (Circle (m, 1/60, EARTH_CIRCUMFERENCE))
        return CircleCollection (c_l).get_map_developers_string ()

class SightTrip:
    ''' Object used for dead-reckoning. Sights are taken on different times
        Course and speed are estimated input parameters.  '''
#pylint: disable=R0913
    def __init__ (self, \
                       sight_start : Sight | datetime,
                       sight_end : Sight,
                       estimated_starting_point : LatLonGeodetic,
                       course_degrees : int | float,
                       speed_knots : int | float):
        self.sight_start              = sight_start
        self.sight_end                = sight_end
        self.estimated_starting_point = estimated_starting_point.get_latlon()
        self.course_degrees           = course_degrees
        self.speed_knots              = speed_knots
        self.__calculate_time_hours ()
        self.movement_vec             = None
        self.start_pos                = None
        self.end_pos                  = None
        self.mapping_distance       = None
#pylint: enable=R0913

    def __calculate_time_hours (self):
        if isinstance (self.sight_start, Sight):
            dt1 = self.sight_start.set_time_dt
        else:
            dt1 = self.sight_start
        dt2 = self.sight_end.set_time_dt
        self.time_hours = calculate_time_hours (dt1, dt2)

    def __calculate_distance_to_target (self, angle : int | float,
                                        a_vec : list [float], b_vec : list [float])\
          -> tuple [float, LatLon, LatLon]:
        rotation_angle = deg_to_rad (angle)
        rotated_vec = rotate_vector (b_vec, a_vec, rotation_angle)
        rotated_latlon = to_latlon (rotated_vec)
        taken_out = takeout_course (rotated_latlon, self.course_degrees,\
                                   self.speed_knots, self.time_hours)

        dbp = spherical_distance\
              (taken_out, self.sight_end.gp)\
                  - self.sight_end.get_circle(geodetic=False).get_radius()
        return dbp, taken_out, rotated_latlon

    def set_mapping_distance (self, distance : float | NoneType):
        ''' Attach a mapping distance estimation '''
        self.mapping_distance = distance

    def get_mapping_distance (self) -> float | NoneType:
        ''' Get the current mapping distance estimation '''
        return self.mapping_distance

#pylint: disable=R0914
    def get_intersections (self, return_geodetic : bool, diagnostics : bool = False) ->\
            tuple[LatLon | tuple[LatLon, LatLon], float, str]:
        ''' Get the intersections for this sight trip object '''            

        ### Calculate a trip from Sight to Sight
        if isinstance (self.sight_start, Sight):

            # Calculate intersections
            pair = SightPair (self.sight_start, self.sight_end)
            best_intersection, fitness, diag_output = pair.get_intersections\
                (return_geodetic=False,
                 estimated_position = self.estimated_starting_point,\
                 diagnostics = diagnostics)
            # Determine angle of the intersection point on sight_start small circle
            a_vec = to_rectangular (self.sight_start.gp)
            assert isinstance (best_intersection, LatLon)
            b_vec = to_rectangular (best_intersection)

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
                raise IntersectError ("Cannot calculate a trip vector")
            assert taken_out is not None
            assert rotated is not None
            self.start_pos = rotated
            self.end_pos   = taken_out
            if return_geodetic:
                taken_out = LatLonGeodetic (ll=taken_out)
                rotated   = LatLonGeodetic (ll=rotated)
            return (taken_out, rotated), fitness, diag_output

        ### Calculate a trip from a timestamp (with estimated position) to Sight
        # isinstance (self.sight_start, datetime) == True
        taken_out = takeout_course (self.estimated_starting_point,\
                                    self.course_degrees,\
                                    self.speed_knots, self.time_hours)
        assert isinstance (taken_out, LatLon)
        circle1 = Circle (self.sight_end.gp,
                          self.sight_end.get_angle(geodetic = False),
                          EARTH_CIRCUMFERENCE)

        circle2 = get_great_circle_route (taken_out, self.sight_end.gp)

        assert isinstance (circle2, Circle)
        self.movement_vec = circle2.latlon
        gi, fitness, diag = get_intersections \
                           (circle1, circle2,
                            estimated_position=taken_out)

        assert isinstance (gi, LatLon)
        self.set_mapping_distance (circle2.get_mapping_distance ())
        self.sight_end.set_mapping_distance (circle1.get_mapping_distance())
        self.start_pos = self.estimated_starting_point
        self.end_pos = gi
        if return_geodetic:
            gi = LatLonGeodetic (ll=gi)
        return gi, fitness, diag
#pylint: enable=R0914

    def get_map_developers_string (self) -> str:
        '''
        Return URL for https://mapdevelopers.com circle plotting service
        '''
        if isinstance (self.sight_start, Sight):
            s_c = SightCollection ([self.sight_start, self.sight_end])
            if isinstance (self.start_pos, LatLon) and isinstance (self.end_pos, LatLon):
                return s_c.get_map_developers_string\
                        (geodetic = True,\
                         markers = \
                        [LatLonGeodetic(ll = self.start_pos), \
                         LatLonGeodetic(ll = self.end_pos)])
            else:
                return s_c.get_map_developers_string (geodetic=True)

        # isinstance (self.sight_start, LatLon) == True
        assert isinstance (self.movement_vec, LatLon)

        # Plot the end sight
        str1 = self.sight_end.get_map_developers_string (include_url_start=False, geodetic = True)

        # Plot the great circle
        d = self.get_mapping_distance()
        assert isinstance (d, float) or d is None
        str2 = get_map_developers_string\
              (EARTH_CIRCUMFERENCE/4, LatLonGeodetic(ll=self.movement_vec), distance=d)
        url_start = MAP_DEV_URL
        result = "["
        result += str1
        result += ","
        result += str2

        # Handle/plot markers
        if isinstance (self.start_pos, LatLon) and isinstance (self.end_pos, LatLon):
            result += ","
            result += get_map_developers_string (1, LatLonGeodetic(ll=self.start_pos))
            result += ","
            result += get_map_developers_string (1, LatLonGeodetic(ll=self.end_pos))
        result += "]"
        result = quote_plus (result)
        return url_start + result
