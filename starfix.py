''' A toolkit for celestial navigation, in particular sight reductions 
    © August Linnman, 2024, email: august@linnman.net
    MIT License (see LICENSE file)
'''

from math import  pi, sin, cos, acos, sqrt, tan, atan2
from datetime import datetime
from urllib.parse import quote_plus
from types import NoneType

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
        return "LAT = " + str(round(self.lat,4)) + "; LON = " + str(round(self.lon,4))

    def get_tuple (self) -> tuple[float | int, float | int] :
        ''' Used to simplify some code where tuples are more practical '''
        return self.lon, self.lat

# Utility routines (algrebraic, spheric geometry)

def add_vecs (vec1 : list[float], vec2 : list[float]) -> list[float]:
    ''' Performs addition of two cartesian vectors '''
    assert len (vec1) == len (vec2)
    retval = []
    for i, v in enumerate(vec1):
        retval.append (v + vec2[i])
    return retval

def subtract_vecs (vec1 : list[float], vec2 : list[float]) -> list [float]:
    ''' Performs subtraction of two cartesian vectors '''
    assert len (vec1) == len (vec2)
    return add_vecs (vec1, mult_scalar_vect(-1, vec2))

def mult_scalar_vect (scalar : int | float, vec : list [float]) -> list [float]:
    ''' Performs multiplication of a cartesian vector with a scalar '''
    retval = []
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
    a_vec = []
    a_vec.append (cos (theta) * sin (phi))
    a_vec.append (sin (theta) * sin (phi))
    a_vec.append (cos (phi))
    a_vec = normalize_vect (a_vec)
    return a_vec

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
    ''' Calculates the angle between two points on Earth 
        Return : Angle in radians '''
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

#pylint: disable=R0903
class Sextant:
    ''' This class represents a physical sextant, with various errors '''
    def __init__  (self, graduation_error : float):
        self.graduation_error = graduation_error
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
    def __init__ (self, set_time : str, set_time_deviation_seconds : int | float, \
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

def get_dip_of_horizon (hm : int | float, temperature : float, dt_dh : float, pressure : float)\
      -> float:
    ''' Calculate dip of horizon in arc minutes 
    Parameters:
        hm : height in meters
        temperature : temperature in degrees Celsius
        dt_th : temperature gradient in degrees Celsius / meter
    '''
    k_factor = 503*(pressure*10)*(1/((temperature+273)**2))*(0.0343 + dt_dh)
    h = hm / 1000
    r = EARTH_RADIUS
    rr = r / (1 - k_factor)
    the_dip = (acos (rr/(rr+h)))*(180/pi)*60
    return the_dip

# Intersections

class IntersectError (ValueError):
    ''' Exception used for failed intersections '''

    def __init__ (self, info : str):
        super().__init__ (info)

#pylint: disable=R0912
#pylint: disable=R0913
#pylint: disable=R0914
#pylint: disable=R0915
def get_intersections (latlon1 : LatLon, latlon2 : LatLon,\
                       angle1 : int | float, angle2 : int | float,\
                       estimated_position : NoneType | LatLon = None,\
                       use_fitness : bool = True, diagnostics : bool = False,
                       intersection_number : int = 0)\
                          -> tuple[LatLon | tuple[LatLon, LatLon], float, str]:
    '''
    Get intersection of two circles on a spheric surface. 
    At least one of the circles must be a small circle. 
https://math.stackexchange.com/questions/4510171/how-to-find-the-intersection-of-two-circles-on-a-sphere 
    Parameters:
        latlon1 : GP nr 1 location
        latlon2 : GP nr 2 location
        angle1 : Angle from zenith of star fix 1 (in radians)
        angle2 : Angle from zenith of star fix 2 (in radians)
        estimated_position : A DRP position, if available. Set to None if unknown. 
        use_fitness : Set to True if fitness calculation is requested.
        diagnostics : Set to True if diagnostics is required. Diagnostics is returned as the third item in return value tuple. 
        intersection_number : Used for diagnostics to label output. 
    '''
    assert angle1 >= 0 and angle2 >= 0
    assert angle1 < 90 or angle2 < 90  # Make sure one of the circles is a small circle
    diag_output = ""
    # Get cartesian vectors a and b (from ground points)
    if diagnostics:
        if intersection_number != 0:
            diag_output += "\n## Performing an intersection (#"+str(intersection_number)+")\n\n"
        else:
            diag_output += "\n## Performing an intersection\n\n"
        diag_output += "### **Input parameters**\n"
        diag_output +=\
        "$\\textbf{latlon1}=("+str(round(latlon1.lat,4))+","+str(round(latlon1.lon,4))+")$<br/>"
        diag_output +=\
        "$\\textbf{angle1}=("+str(round(angle1,4))+")$<br/>"        
        diag_output +=\
        "$\\textbf{latlon2}=("+str(round(latlon2.lat,4))+","+str(round(latlon2.lon,4))+")$<br/>"        
        diag_output +=\
        "$\\textbf{angle2}=("+str(round(angle2,4))+")$<br/>"
        if estimated_position is not None:
            diag_output +=\
            "$\\textbf{EstimatedPosition}=("+\
                str(round(estimated_position.lat,4))+","+\
                str(round(estimated_position.lon,4))+")$<br/>"
    a_vec = to_rectangular (latlon1)
    b_vec = to_rectangular (latlon2)
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
    p1 = mult_scalar_vect (cos(deg_to_rad(angle2)), a_vec)
    if diagnostics:
        diag_output +=\
        "* We compute $\\text{p1}$\n"
        diag_output += "    * $cos(\\text{angle1})\\cdot\\text{aVec} = ("+\
            str(round(p1[0],4))+","+\
            str(round(p1[1],4))+","+\
            str(round(p1[2],4))+")\\text{ ==> }\\textbf{p1}"+\
            "$\n"
    p2 = mult_scalar_vect (-cos(deg_to_rad(angle1)), b_vec)
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
        if angle1 < angle2:
            rho = acos (cos (deg_to_rad(angle1)) / (dot_product (a_vec, q)))
            if diagnostics:
                diag_output +=\
                "* $\\arccos{\\left(\\frac {\\cos{\\left(\\text{angle1}\\right)}}"+\
                "{\\text{aVec}\\cdot\\text{q}}\\right)}"
        else:
            rho = acos (cos (deg_to_rad(angle2)) / (dot_product (b_vec, q)))
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
        return ret_tuple, fitness, diag_output
    else:
        # Check which of the intersections is closest to our estimatedCoordinates
        best_distance = EARTH_CIRCUMFERENCE
        best_intersection = None
        for ints in ret_tuple:
            the_distance = distance_between_points (ints, estimated_position)
            if the_distance < best_distance:
                best_distance = the_distance
                best_intersection = ints
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

#pylint: disable=R1710
def get_google_map_string (intersections : tuple | LatLon, num_decimals : int) -> str :
    ''' Return a coordinate which can be used in Google Maps '''
    if isinstance (intersections, LatLon):
        return str(round(intersections.lat,num_decimals)) + "," +\
               str(round(intersections.lon,num_decimals))
    if isinstance (intersections, tuple):
        assert len (intersections) == 2
        return get_google_map_string (intersections[0], num_decimals) + ";" + \
               get_google_map_string (intersections[1], num_decimals)
#pylint: enable=R1710

def get_representation\
    (ins : LatLon | tuple | list | float | int, num_decimals : int, lat=False) -> str:
    ''' Converts coordinate(s) to a string representation '''
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
    raise ValueError ("Incorrect types for representation.")

def parse_angle_string (angle_string : str) -> float:
    ''' Read a string "DD:MM:SS" and return a decimal degree value.
        Minute and second specifications are optional. 
        Decimal values can be used. '''
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

#pylint: disable=R0913
def get_terrestrial_position (point_a1 : LatLon,\
                              point_a2 : LatLon,\
                              angle_a : int | float,\
                              point_b1 : LatLon,\
                              point_b2 : LatLon,\
                              angle_b : int | float,
                              estimated_position : LatLon | NoneType = None,\
                              diagnostics : bool = False)\
            -> tuple [LatLon | tuple, LatLon, float, LatLon, float, float, str] :
    '''
    Given two pairs of terrestial observations (pos + angle) determine the observer's position 
    '''

    a = get_circle_for_angle (point_a1, point_a2, angle_a)
    b = get_circle_for_angle (point_b1, point_b2, angle_b)
    # Finally compute the intersection.
    # Since we require an estimated position we will eliminate the false intersection.
    intersection, fitness, diag_output =\
        get_intersections (a[0], b[0], a[1], b[1], estimated_position, diagnostics)
    return intersection, a[0], a[1], b[0], b[1], fitness, diag_output
#pylint: enable=R0913

# Celestial Navigation

#pylint: disable=R0902
class Sight :
    '''  Object representing a sight (star fix) '''
#pylint: disable=R0912
#pylint: disable=R0913
#pylint: disable=R0914
    def __init__ (self, \
                  object_name              : str, \
                  set_time                 : str, \
                  gha_time_0               : str,\
                  gha_time_1               : str,\
                  decl_time_0              : str, \
                  measured_alt             : str,\
                  decl_time_1              : NoneType | str = None, \
                  sha_diff                 : NoneType | str = None, \
                  observer_height          : int | float = 0, \
                  artificial_horizon       : bool = False, \
                  index_error_minutes      : int = 0, \
                  semi_diameter_correction : int | float = 0,\
                  horizontal_parallax      : int | float = 0,\
                  sextant                  : NoneType | Sextant = None,\
                  chronometer              : NoneType | Chronometer = None,\
                  temperature              : float = 10.0,\
                  dt_dh                    : float = -0.01,\
                  pressure                 : float = 101.0,
                  ho_obs                   : bool = False):
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
        self.decl_time_0           = parse_angle_string (decl_time_0)
        self.decl_time_1           = parse_angle_string (decl_time_1)
        if self.decl_time_0 < -90 or self.decl_time_0 > 90 or \
           self.decl_time_1 < -90 or self.decl_time_1 > 90:
            raise ValueError ("Declination values must be within [-90,90]")
        self.measured_alt          = parse_angle_string (measured_alt)
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
            self.__correct_for_graduation_error (sextant)
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
            self.__correct_dip_of_horizon ()
        self.gp = self.__calculate_gp ()
#pylint: enable=R0912
#pylint: enable=R0913
#pylint: enable=R0914

    def __correct_set_time (self, chronometer : Chronometer):
        dt1 = self.set_time_dt
        dt2 = chronometer.get_corrected_time (dt1)
        self.set_time_dt = dt2

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

        min_sec_contribution = self.set_time_dt.minute/60 + self.set_time_dt.second/3600

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

    def get_azimuth (self, from_pos : LatLon) -> float:
        ''' Return the azimuth of this sight (to the GP) from a particular point on Earth 
            Returns the azimuth in degrees (0-360)'''
        return get_azimuth (self.gp, from_pos)
#pylint: enable=R0902

#pylint: disable=R0903
class SightPair:
    ''' Represents a pair of sights, needed for making a sight reduction '''
    def __init__ (self, sf1 : Sight, sf2 : Sight):
        self.sf1 = sf1
        self.sf2 = sf2

    def get_intersections (self, estimated_position : NoneType | LatLon = None,\
                           diagnostics : bool = False,\
                           intersection_number : int = 0) ->\
                           tuple[LatLon | tuple[LatLon, LatLon], float, str]:
        ''' Return the two intersections for this sight pair. 
            The parameter estimated_position can be used to eliminate the false intersection '''
        return get_intersections (self.sf1.gp,\
                                  self.sf2.gp,\
                                  self.sf1.get_angle(), self.sf2.get_angle(),\
                                  estimated_position, diagnostics = diagnostics,\
                                  intersection_number = intersection_number)
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
        (self, limit : int | float = 100,\
          estimated_position : NoneType | LatLon = None,\
          diagnostics : bool = False) \
            -> tuple[LatLon | tuple[LatLon, LatLon], float, str]:
        ''' Get an intersection from the collection of sights. 
            A mean value and sorting algorithm is applied. '''
        diag_output = ""
        nr_of_fixes = len(self.sf_list)
        assert nr_of_fixes >= 2
        if nr_of_fixes == 2:
            # For two star fixes just use the algorithm of SightPair.getIntersections
            return SightPair (self.sf_list[0],\
                              self.sf_list[1]).get_intersections\
                                         (estimated_position, diagnostics = diagnostics)
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
                    p.get_intersections (estimated_position, diagnostics = diagnostics,\
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
                    dist = distance_between_points (coords[i][0], coords[j][0])
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
                        dist = distance_between_points (coords[0][cp1], coords[0][cp2])
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
            fitness_here   = coords [cp][1]
            fitness_sum += fitness_here
            rect_vec = to_rectangular (selected_coord)
            summation_vec =\
                add_vecs (summation_vec,\
                mult_scalar_vect ((1/nr_of_chosen_points)*fitness_here, rect_vec))
        summation_vec = normalize_vect (summation_vec)
        return to_latlon (summation_vec), fitness_sum, diag_output
#pylint: enable=R0912
#pylint: enable=R0914
#pylint: enable=R0915

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
#pylint: disable=R0913
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
#pylint: enable=R0913

    def __calculate_time_hours (self):
        dt1 = self.sight_start.set_time_dt
        it1 = int(dt1.timestamp())
        dt2 = self.sight_end.set_time_dt
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

#pylint: disable=R0914
    def get_intersections (self, diagnostics : bool = False) ->\
            tuple[LatLon | tuple[LatLon, LatLon], float, str]:
        ''' Get the intersections for this sight trip object '''
        # Calculate intersections
        pair = SightPair (self.sight_start, self.sight_end)
        best_intersection, fitness, diag_output = pair.get_intersections\
              (estimated_position = self.estimated_starting_point, diagnostics = diagnostics)
        # Determine angle of the intersection point on sightStart small circle
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
        return (taken_out, rotated), fitness, diag_output
#pylint: enable=R0914

    def get_map_developers_string (self) -> str:
        '''
        Return URL for https://mapdevelopers.com circle plotting service
        '''
        s_c = SightCollection ([self.sight_start, self.sight_end])
        return s_c.get_map_developers_string ()
