''' A toolkit for celestial navigation, in particular sight reductions 
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)
'''

import sys
from sys import version_info
from math import  pi, sin, cos, acos, sqrt, tan, atan2
from random import gauss
from datetime import datetime, date, timedelta, timezone
from types import NoneType
from collections.abc import Callable

import subprocess
from multiprocessing import Process
import webbrowser

################################################
# Metadata and file access
################################################

PANDAS_INITIALIZED = False
try:
#pylint: disable=W0611
    import pandas
#pylint: enable=W0611
    PANDAS_INITIALIZED = True
except ModuleNotFoundError:
    pass

try:
#pylint: disable=W0611
    from offline_folium import offline
#pylint: enable=W0611
except ModuleNotFoundError:
    pass
except ImportError:
    pass

FOLIUM_INITIALIZED = False
try:
#pylint: disable=W0611
    import folium
#pylint: enable=W0611
    FOLIUM_INITIALIZED = True
except ModuleNotFoundError:
    pass
except ImportError:
    pass

def check_folium ():
    ''' Check if folium is installed. Otherwise abort with exception '''
    if not FOLIUM_INITIALIZED:
        raise ValueError\
            ("Folium not available. Cannot generate maps. "+\
            "Install folium with \"pip install folium\"")

def folium_initialized ():
    ''' Can be used to check if folium is initialized '''
    return FOLIUM_INITIALIZED

def __version_warning (min_major_ver : int, min_minor_ver : int):
    ''' Check compatible Python version '''

    def output_warning ():
        print ("WARNING: You should use Python " +\
            str(min_major_ver) + "." +str (min_minor_ver)+" for this toolkit!")

    major_version = version_info[0]
    if major_version < min_major_ver:
        output_warning ()
    elif major_version == min_major_ver:
        minor_version = version_info[1]
        if minor_version < min_minor_ver:
            output_warning ()

__version_warning (3, 11)

def __run_http_server ():
    if __is_android():
        subprocess.run (["python", "-m", "http.server", "8000"],\
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,\
                        check=False)

def __is_android () -> bool:
    if hasattr(sys, 'getandroidapilevel'):
        return True
    return False

def show_or_display_file (filename : str):
    ''' Used to display a file (typically a map) '''
    linkname = "http://localhost:8000/" + filename
    if __is_android ():
        print ("Press this link ---> " + linkname)
    else:
        webbrowser.open (filename)

def __start_http_server ():
    if __is_android():
        p = Process(target=__run_http_server)
        p.start()

__start_http_server ()


################################################
# Dimension of Earth
################################################

EARTH_CIRCUMFERENCE_EQUATORIAL = 40075.017
EARTH_CIRCUMFERENCE_MERIDIONAL = 40007.86
EARTH_CIRCUMFERENCE = (EARTH_CIRCUMFERENCE_EQUATORIAL*2 + EARTH_CIRCUMFERENCE_MERIDIONAL) / 3
EARTH_RADIUS = EARTH_CIRCUMFERENCE / (2 * pi)


EARTH_RADIUS_GEODETIC_EQUATORIAL = 6378
EARTH_RADIUS_GEODETIC_POLAR      = 6357
EARTH_FLATTENING =\
    (EARTH_RADIUS_GEODETIC_EQUATORIAL - EARTH_RADIUS_GEODETIC_POLAR) / \
     EARTH_RADIUS_GEODETIC_EQUATORIAL

################################################
# Data types
################################################

class LatLon:
    ''' Base class for lat-lon pairs '''
    def __init__ (self, lat : float | int, lon : float | int):
        assert -90 <= lat <= 90
        self.__lat = lat
        self.__lon = mod_lon(lon)

    def get_tuple (self) -> tuple[float | int, float | int] :
        ''' Used to simplify some code where tuples are more practical '''
        return self.__lon, self.__lat

    def get_lat (self) -> int | float:
        ''' Returns the latitude '''
        return self.__lat

    def get_lon (self) -> int | float:
        ''' Returns the longitude '''
        return self.__lon

class LatLonGeocentric (LatLon):
    ''' Represents spherical coordinates on Earth '''

    def __str__(self):
        return "(Geocentric) LAT = " +\
               str(round(self.get_lat(),4)) +\
               "; LON = " + str(round(self.get_lon(),4))

################################################
# Utility routines (algrebraic, spheric geometry)
################################################

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

def mod_lon (lon : int | float) -> int | float:
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

def to_latlon (vec : list [float]) -> LatLonGeocentric:
    ''' Convert cartesian coordinate to LatLon (spherical) '''
    assert len (vec) == 3
    vec = normalize_vect (vec)

    theta = atan2 (vec[1],vec[0])
    phi = acos (vec[2])
    lon = rad_to_deg (theta)
    lat = 90-rad_to_deg (phi)

    return LatLonGeocentric (lat, mod_lon(lon))

def to_rectangular (latlon : LatLon) -> list [float]:
    ''' Convert LatLon (spherical) coordinate to cartesian '''
    phi = deg_to_rad (90 - latlon.get_lat())
    theta = deg_to_rad (latlon.get_lon())
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

def squeeze (val : float, min_val : float, max_val : float) -> float :
    ''' Used to limit a value in a range/interval '''
    if val > max_val:
        return max_val
    if val < min_val:
        return min_val
    return val

################################################
# Course management
################################################

def mod_course (lon : int | float) -> float:
    ''' Transform a course angle into the compass range of (0,360) '''
    x = lon % 360
    return x

def takeout_course (latlon : LatLonGeocentric, course : int | float, speed_knots : int | float,
                    time_hours : int | float) -> LatLonGeocentric:
    ''' Calculates a trip movement. Simplified formula, not using great circles '''
    distance = speed_knots * time_hours
    distance_degrees = distance / 60
    # The "stretch" is just taking care of narrowing longitudes on higher latitudes
    stretch_at_start = cos (deg_to_rad (latlon.get_lat()))
    diff_lat = cos (deg_to_rad(course))*distance_degrees
    diff_lon = sin (deg_to_rad(course))*distance_degrees/stretch_at_start
    return LatLonGeocentric (latlon.get_lat()+diff_lat, latlon.get_lon()+diff_lon)

def angle_b_points (latlon1 : LatLon, latlon2 : LatLon) -> float:
    ''' Calculates the angle between two points on Earth 
        Return : Angle in radians '''
    normvec1 = to_rectangular (latlon1)
    normvec2 = to_rectangular (latlon2)
    dp = dot_product (normvec1, normvec2)
    # Taking care of occasional rounding errors.
    # acos breaks if the |dp| is something like 1.000000000000001
    # Thanks to https://github.com/0dB for finding this bug.
    dp = squeeze (dp, -1, 1)
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

################################################
# Sextant calibration
################################################

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

def angle_between_points (origin : LatLonGeocentric,
                          point1 : LatLonGeocentric, point2 : LatLonGeocentric) -> float:
    ''' Return the angle in degrees between two terrestrial targets (point1 and point2) 
        as seen from the observation point (origin) '''
    origin_r = to_rectangular (origin)
    point_1r = to_rectangular (point1)
    point_2r = to_rectangular (point2)

    point_1gc = normalize_vect (cross_product (origin_r, point_1r))
    point_2gc = normalize_vect (cross_product (origin_r, point_2r))
    dp = dot_product (point_1gc, point_2gc)
    return acos (dp) * (180 / pi)

################################################
# Chronometer
################################################

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
        return datetime.fromtimestamp (mt_corr, tz = measured_time.tzinfo)
# pylint: enable=R0903

################################################
# Horizon
################################################

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

################################################
# Intersections
################################################

#pylint: disable=R0903
class Circle:
    ''' Helper class for circles (great or small circles) '''

    def __init__ (self, latlon : LatLon, angle : int | float,
                  circumference : float = EARTH_CIRCUMFERENCE):
        ''' Parameters:
                latlon        : centerpoint
                angle         : angle of circle in degrees, for a great circle set to 90
                circumference : the circumference of the sphere (Earth)
        '''
        self.__latlon                 = latlon
        self.__angle                = angle
        self.__circumference        = circumference

    def get_angle (self) -> int | float :
        ''' Return the angle (in degrees) of this circle '''
        return self.__angle

    def get_latlon (self) -> LatLon:
        ''' Return the latlon of this circle '''
        return self.__latlon

    def make_geodetic (self) :
        ''' Convert this circle to a geodetic latlon '''
        if isinstance (self.__latlon, LatLonGeodetic):
            pass
        else:
            self.__latlon = LatLonGeodetic (ll=self.__latlon)
        return self

    def __str__(self) -> str:
        return "CIRCLE: LATLON = [" + \
        str(self.__latlon) + "]; ANGLE = " + str(round(self.__angle,4))

#pylint: disable=R0914
    def render_folium (self, the_map : object, color : str = "#FF0000",
                       adjust_geodetic : bool = True):
        ''' Renders a circle on a folium map '''

        def adapt_lon (input_lon : float, center_lon : float) -> float:
            diff = input_lon - center_lon
            if abs(diff) >= 180:
                if center_lon > 0:
                    diff = diff + 360
                else:
                    diff = diff - 360
            return center_lon + diff

        check_folium ()

        coordinates = list [list[float]]()
        sub_coord = []

#pylint: disable=C0415
        from folium import PolyLine, Map
#pylint: enable=C0415
        assert isinstance (the_map, Map)

        b = to_rectangular (self.get_latlon ())
        north_pole = [0.0, 0.0, 1.0] # to_rectangular (LatLon (90, 0))
        east_tangent = normalize_vect(cross_product (north_pole, b))
        north_tangent = normalize_vect (cross_product (b, east_tangent))
        c_latlon = self.get_latlon ()
        # assert isinstance (self, Circle)
        degrees_10 = 0
        last_lon = None
        while degrees_10 <= 3600:
            # A PolyLine with 0.1 degrees separation is smooth enough
            angle = degrees_10 / 10.0
            degrees_10 += 1
            real_tangent =\
                add_vecs (\
                            mult_scalar_vect (-cos(deg_to_rad(angle)), east_tangent),
                            mult_scalar_vect (sin(deg_to_rad(angle)), north_tangent)
                            )
            y = rotate_vector (b, real_tangent, deg_to_rad(self.get_angle()))

            y_latlon = to_latlon (y)
            if adjust_geodetic:
                y_geodetic = LatLonGeodetic (ll = y_latlon)
                y_target = y_geodetic
            else:
                y_target = y_latlon
            this_lon = adapt_lon(y_target.get_lon(), c_latlon.get_lon())
            # Avoid jagged lines
            if last_lon is not None and\
                abs (this_lon - last_lon) > 10 and\
                len(sub_coord) > 0:
                coordinates.append (sub_coord)
                # Flush out current PolyLine
                PolyLine(
                    locations=coordinates,
                    color=color,
                    weight=5,
                    popup="Small circle"
                ).add_to(the_map)
                # Reset variables
                coordinates = list [list[float]]()
                sub_coord = []
                last_lon = None
            else:
                sub_coord.append\
                        ([y_target.get_lat(), this_lon])
            last_lon = this_lon
        coordinates.append (sub_coord)
        PolyLine(
            locations=coordinates,
            color=color,
            weight=5,
            popup="Small circle"
        ).add_to(the_map)
#pylint: enable=R0914

    def get_radius (self) -> float:
        ''' Returns the radius of the sight (in kilometers) '''
        return (self.__angle/360)*self.__circumference

class CircleCollection:
    ''' Simple collection of circles '''
    def __init__ (self, coll : list[Circle]):
        self.c_list = coll

    def make_geodetic (self):
        ''' Convert this collection to geodetic '''
        for c in self.c_list:
            c.make_geodetic ()
        return self

    def render_folium (self, center_pos : LatLon,\
                       colors : list[str] | NoneType = None,
                       adjust_geodetic : bool = True) -> object :
        ''' Render this circle collection in Folium '''
        check_folium ()
#pylint: disable=C0415
        from folium import Map
#pylint: enable=C0415
        the_map = Map (location=[center_pos.get_lat(), center_pos.get_lon()])
        l = len (self.c_list)
        for i in range (l):
            color = "#FF0000"
            if colors is not None:
                color = colors [i]
            self.c_list[i].render_folium (the_map, color, adjust_geodetic=adjust_geodetic)
        return the_map

#pylint: enable=R0903

#pylint: disable=R0914
def get_great_circle_route\
     (start : LatLon, direction : LatLon | float | int,
      convert_to_geocentric : bool = True) -> Circle:
    ''' Calculates a great circle starting in 'start' 
        and passing 'direction' coordinate (if LatLon) 
        or with direction 'direction' degrees (if float or int)    
    '''
#pylint: disable=C0123
    if isinstance (direction, LatLonGeocentric):
        assert type(start) == type(direction)
#pylint: enable=C0123

    converted = False
    if convert_to_geocentric and isinstance (start, LatLonGeodetic):
        start = start.get_latlon()
        converted = True
#pylint: disable=C0123
        assert type(start) == LatLonGeocentric
        if isinstance (direction, LatLonGeodetic):
            direction = direction.get_latlon()
            assert type(direction) == LatLonGeocentric
#pylint: enable=C0123

    if isinstance (direction, LatLonGeocentric):
        t1 = to_rectangular (start)
        t2 = to_rectangular (direction)
        t3 = normalize_vect(cross_product (t1,t2))
        t4 = to_latlon (t3)
        if converted:
            t4 = LatLonGeodetic (ll=t4)
        c = Circle (t4, 90, EARTH_CIRCUMFERENCE)
        return c
    # isinstance (direction, float) or isinstance (direction, int) == True

    assert isinstance (direction, (float, int))
    if start.get_lat() in (90,-90):
        raise ValueError ("Cannot take a course from any of the poles")

    # Made a new (simpler) implementation
    assert isinstance (start, LatLonGeocentric)
    assert isinstance (direction, (float, int))
    goto_pos = takeout_course (start, direction, 1, 1)
    start_xyz = to_rectangular (start)
    goto_xyz  = to_rectangular (goto_pos)
    cp = cross_product (start_xyz, goto_xyz)
    cp_pos = to_latlon (cp)
    #cp_pos = LatLonGeodetic (ll=cp_pos)
    return Circle (latlon = cp_pos, angle=90, circumference=EARTH_CIRCUMFERENCE)

    # Leaving old implementation here
    #north_pole = [0.0, 0.0, 1.0] # to_rectangular (LatLon (90, 0))
    #b = to_rectangular (start)
    #east_tangent = normalize_vect(cross_product (b, north_pole))
    #rotated = rotate_vector (east_tangent, b, deg_to_rad(90 - direction))
    #cp = normalize_vect(cross_product (b, rotated))
    #cp_latlon = to_latlon (cp)
    #if converted:
    #    cp_latlon = LatLonGeodetic (ll = cp_latlon)
    #c = Circle (cp_latlon, 90, EARTH_CIRCUMFERENCE)
    #return c
#pylint: enable=R0914

class IntersectError (ValueError):
    ''' Exception used for failed intersections '''

    def __init__ (self, info : str, coll : object = None):
        super().__init__ (info)
        self.coll_object = coll

#pylint: disable=R0912
#pylint: disable=R0913
#pylint: disable=R0914
#pylint: disable=R0915
#pylint: disable=R0917
def get_intersections (circle1 : Circle, circle2 : Circle,
                       estimated_position : NoneType | LatLon = None,
                       use_fitness : bool = True, diagnostics : bool = False,
                       intersection_number : int = 0) \
                          -> tuple[
                              LatLonGeocentric | tuple[LatLonGeocentric, LatLonGeocentric],
                              # Coordinate or Coordinate Pair
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
    assert circle1.get_angle() >= 0 and circle2.get_angle() >= 0

    # Handle intersection of two great circles
    if circle1.get_angle() == 90 and circle2.get_angle() == 90:
        a_vec = to_rectangular (circle1.get_latlon())
        b_vec = to_rectangular (circle2.get_latlon())
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
            return ret_tuple, fitness, diag_output

        # Check which of the intersections is closest to our estimatedCoordinates
        best_distance = EARTH_CIRCUMFERENCE
        best_intersection = None
        for ints in ret_tuple:
            the_distance = spherical_distance (ints, estimated_position)
            if the_distance < best_distance:
                best_distance = the_distance
                best_intersection = ints
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
        "$\\textbf{latlon1}=("+str(round(circle1.get_latlon().get_lat(),4))+","+\
            str(round(circle1.get_latlon().get_lon(),4))+")$<br/>"
        diag_output +=\
        "$\\textbf{angle1}=("+str(round(circle1.get_angle(),4))+")$<br/>"        
        diag_output +=\
        "$\\textbf{latlon2}=("+str(round(circle2.get_latlon().get_lat(),4))+","+\
            str(round(circle2.get_latlon().get_lon(),4))+")$<br/>"
        diag_output +=\
        "$\\textbf{angle2}=("+str(round(circle2.get_angle(),4))+")$<br/>"
        if estimated_position is not None:
            diag_output +=\
            "$\\textbf{EstimatedPosition}=("+\
                str(round(estimated_position.get_lat(),4))+","+\
                str(round(estimated_position.get_lon(),4))+")$<br/>"
    a_vec = to_rectangular (circle1.get_latlon())
    b_vec = to_rectangular (circle2.get_latlon())
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
    p1 = mult_scalar_vect (cos(deg_to_rad(circle2.get_angle())), a_vec)
    if diagnostics:
        diag_output +=\
        "* We compute $\\text{p1}$\n"
        diag_output += "    * $cos(\\text{angle1})\\cdot\\text{aVec} = ("+\
            str(round(p1[0],4))+","+\
            str(round(p1[1],4))+","+\
            str(round(p1[2],4))+")\\text{ ==> }\\textbf{p1}"+\
            "$\n"
    p2 = mult_scalar_vect (-cos(deg_to_rad(circle1.get_angle())), b_vec)
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

    if circle1.get_angle() < circle2.get_angle():
        try:
            rho = acos (cos (deg_to_rad(circle1.get_angle())) / (dot_product (a_vec, q)))
        except ValueError as ve:
            raise IntersectError ("Small circles don't intersect") from ve
        if diagnostics:
            diag_output +=\
            "* $\\arccos{\\left(\\frac {\\cos{\\left(\\text{angle1}\\right)}}"+\
            "{\\text{aVec}\\cdot\\text{q}}\\right)}"
    else:
        try:
            rho = acos (cos (deg_to_rad(circle2.get_angle())) / (dot_product (b_vec, q)))
        except ValueError as ve:
            raise IntersectError ("Small circles don't intersect") from ve
        if diagnostics:
            diag_output +=\
            "* $\\arccos{\\left(\\frac {\\cos{\\left(\\text{angle2}\\right)}}"+\
            "{\\text{bVec}\\cdot\\text{q}}\\right)}"
    if diagnostics:
        diag_output += "=" + str(round(rho,4)) + "\\text{ ==> }\\rho$ (rotation angle)\n"

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
        str(round(int1_latlon.get_lat(),4))+","+\
        str(round(int1_latlon.get_lon(),4))+")\\text{ ==> }\\textbf{Intersection 1}$\n"
        diag_output += "    * $\\text{int2}$ converts to $("+\
        str(round(int2_latlon.get_lat(),4))+","+\
        str(round(int2_latlon.get_lon(),4))+")\\text{ ==> }\\textbf{Intersection 2}$\n"
    ret_tuple = (int1_latlon, int2_latlon)

    if estimated_position is None:
        return ret_tuple, fitness, diag_output

    # Check which of the intersections is closest to our estimatedCoordinates
    best_distance = EARTH_CIRCUMFERENCE
    best_intersection = None
    for ints in ret_tuple:
        the_distance = spherical_distance (ints, estimated_position)
        if the_distance < best_distance:
            best_distance = the_distance
            best_intersection = ints
    assert best_intersection is not None
    return best_intersection, fitness, diag_output
#pylint: enable=R0912
#pylint: enable=R0913
#pylint: enable=R0914
#pylint: enable=R0915
#pylint: enable=R0917

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
    if from_pos.get_lat() == 90:
        return (-to_pos.get_lon()) % 360
    if from_pos.get_lat() == -90:
        return to_pos.get_lon() % 360
    # Antipodes have to be handled
    if (to_pos.get_lat() == -from_pos.get_lat()) \
        and (((to_pos.get_lon() - from_pos.get_lon()) % 180) == 0):
        return 0
    # Same coordinate?
    if (to_pos.get_lat() == from_pos.get_lat())\
        and (to_pos.get_lon() == from_pos.get_lon()):
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

################################################
# Time management
################################################

def calculate_time_hours (dt1 : datetime, dt2 : datetime) -> float:
    '''
    Return the difference between two timestamps in hours
    '''
    it1 = int(dt1.timestamp())
    it2 = int(dt2.timestamp())
    return (it2 - it1) / 3600

################################################
# Atmospheric refraction
################################################

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

################################################
# Data formatting
################################################

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
        type_info = ""
#pylint: disable=C0123
        if type(intersections) == LatLonGeodetic:
            type_info = "(Geodetic) "
        elif type(intersections) == LatLonGeocentric:
#pylint: enable=C0123
            type_info = "(Geocentric) "
        type_string = type_info
        return type_string +\
            str(round(intersections.get_lat(),num_decimals)) + "," +\
            str(round(intersections.get_lon(),num_decimals))

    if isinstance (intersections, tuple):
        assert len (intersections) == 2
        return get_google_map_string (intersections[0], num_decimals) + ";" + \
               get_google_map_string (intersections[1], num_decimals)
#pylint: enable=R1710

#pylint: disable=R0912
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
    type_info = ""
    if isinstance (ins, LatLon):
#pylint: disable=C0123
        if type (ins) == LatLonGeocentric:
            type_info = "(Geocentric) "
        elif type (ins) == LatLonGeodetic:
#pylint: enable=C0123
            type_info = "(Geodetic) "
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
        return type_info + prefix + " " + str(a_degrees) + "°," +\
               str(round(minutes, num_decimals)) + "′"
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
        return type_info + ret_val
    # We should never get here
    raise RuntimeError ("Internal processing error")
#pylint: enable=R0912

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

################################################
# Geodetics
################################################

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

        assert lat is None
        assert lon is None

        if isinstance (ll, LatLonGeodetic):
            # Just copy the data from a geodetic coordinate
            super().__init__ (ll.get_lat(), ll.get_lon())
            return

        # ll is a *Geocentrical* coordinate
        # Transforms a geocentric coordinate into geodetic
        #    See: https://www.mathworks.com/help/aeroblks/geocentrictogeodeticlatitude.html
        # See C2D algorithm in README.md
        assert ll is not None
        lam_bda = deg_to_rad (ll.get_lat())
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

        super().__init__(rad_to_deg(mu), ll.get_lon())

    def get_latlon (self, height : float = 0) -> LatLonGeocentric:
        ''' Transforms a geodetic coordinate into geocentric
            See D2C function mentioned in README.md 
            See: https://www.mathworks.com/help/aeroblks/geodetictogeocentriclatitude.html
        '''
        f = EARTH_FLATTENING
        a = EARTH_RADIUS_GEODETIC_EQUATORIAL / (2*pi)
        assert self.get_lat() is not None
        mu = deg_to_rad(self.get_lat())
        e2 = f*(2-f)
        h = height
        n = a / sqrt(1 - e2*(sin(mu))**2)
        rho = (n + h) * cos(mu)
        z = (n*(1 - e2) + h)*sin(mu)
        lam_bda = atan2 (z, rho)
        assert self.get_lon() is not None
        return LatLonGeocentric (rad_to_deg(lam_bda), self.get_lon())

    def __str__(self):
        return "(Geodetic) LAT = " + str(round(self.get_lat(),4)) +\
               "; LON = " + str(round(self.get_lon(),4))


def get_vertical_parallax (llg : LatLonGeodetic) -> tuple [float, LatLonGeocentric]:
    ''' Calculate the vertical parallax 
    (difference between geocentric and geodetic latitude)
    '''
    ll  = llg.get_latlon ()
    llg_rect = to_rectangular (llg)
    ll_rect  = to_rectangular (ll)
    angle    = dot_product (ll_rect, llg_rect)
    return rad_to_deg(acos (angle)), ll

def get_geocentric_alt (position : LatLonGeodetic, geodesic_alt : float,
                        gp : LatLonGeocentric) -> float:
    ''' Convert an estimated geodetic altitude (observation from sextant) to a geocentric value '''
    ang_1 = (pi/2) - acos(dot_product (to_rectangular(position), to_rectangular(gp)))
    epgc = position.get_latlon()
    ang_2 = (pi/2) - acos(dot_product (to_rectangular(epgc),     to_rectangular(gp)))
    diff = rad_to_deg(ang_2 - ang_1)
    return geodesic_alt + diff

def get_geodetic_alt (position : LatLonGeocentric, geocentric_alt : float,
                      gp : LatLonGeocentric) -> float:
    ''' Convert an estimated geocentric altitude to a geodetic value '''
    ang_1 = (pi/2) - acos(dot_product (to_rectangular(position), to_rectangular(gp)))
    epgc = LatLonGeodetic(ll = position)
    ang_2 = (pi/2) - acos(dot_product (to_rectangular(epgc),     to_rectangular(gp)))
    diff = rad_to_deg(ang_2 - ang_1)
    return geocentric_alt + diff

################################################
# Terrestrial Navigation
################################################

def get_circle_for_angle (point1 : LatLonGeodetic, point2 : LatLonGeodetic,
                          angle : int | float)\
      -> Circle :
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
    rot_center_latlon = to_latlon (rot_center)
    radius = rad_to_deg(angle_b_points (to_latlon(rot_center), point1))
    return Circle (LatLonGeodetic(lat=rot_center_latlon.get_lat(),\
                                  lon=rot_center_latlon.get_lon()), radius, EARTH_CIRCUMFERENCE)

#pylint: disable=R0913
#pylint: disable=R0917
def get_terrestrial_position (point_a1 : LatLonGeodetic, # First point pair
                              point_a2 : LatLonGeodetic,
                              angle_a : int | float,     # First angle
                              point_b1 : LatLonGeodetic, # Second point pair
                              point_b2 : LatLonGeodetic,
                              angle_b : int | float,     # Second angle
                              estimated_position : LatLonGeodetic | NoneType = None,
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
#pylint: enable=R0917



################################################
# Machine-Readable Nautical Almanac
################################################

class MrKind:
    ''' Defines root of cel object taxonomy '''
    def __init__ (self, s : str):
        self.kind = s
        MrKind.kind_dict [self.kind] = self
    def __str__ (self):
        return self.kind

    @staticmethod
    def get_kind (s : str) -> object:
        ''' Return a corresponding kind representation '''
        try:
            retval = MrKind.kind_dict [s]
        except KeyError as ke:
            raise ValueError ("Non-existent kind of object") from ke
        assert isinstance (retval, MrKind)
        return retval

    kind_dict = dict[str, object] ()

#pylint: disable=R0903
class MrKindAries (MrKind):
    ''' Used for the position of Aries'''

class MrKindCentral (MrKind):
    ''' Used for Sun and Moon '''

class MrKindPlanet (MrKind):
    ''' Navigational planets '''
#pylint: enable=R0903

class MrKindStar (MrKind):
    ''' Navigational stars '''

    def __init__ (self,s):
        self.index = MrKindStar.star_index
        MrKindStar.star_index += 1
        super().__init__(s)
        MrKindStar.stars [s] = self

    def get_index (self) -> int:
        ''' Return the index of the star in the catalog '''
        return self.index

    @staticmethod
    def is_star (star_name : str) -> bool:
        ''' Check if a name is referring to a star'''
        try:
            _ = MrKindStar.stars [star_name]
            return True
        except KeyError:
            return False

    star_index = 0
    stars = dict [str, object] ()

#pylint: disable=R0903
class CelObjects:
    ''' Dictionary of celestial objects '''
    SUN         = MrKindCentral ("Sun")
    MOON        = MrKindCentral ("Moon")
    ARIES       = MrKindAries ("Aries")
    VENUS       = MrKindPlanet ("Venus")
    MARS        = MrKindPlanet ("Mars")
    JUPITER     = MrKindPlanet ("Jupiter")
    SATURN      = MrKindPlanet ("Saturn")
    Alpheratz   = MrKindStar ("Alpheratz")
    Ankaa       = MrKindStar ("Ankaa")
    Schedar     = MrKindStar ("Schedar")
    Diphda      = MrKindStar ("Diphda")
    Achernar    = MrKindStar ("Achernar")
    Hamal       = MrKindStar ("Hamal")
    Polaris     = MrKindStar ("Polaris")
    Acamar      = MrKindStar ("Acamar")
    Menkar      = MrKindStar ("Menkar")
    Mirfak      = MrKindStar ("Mirfak")
    Aldebaran   = MrKindStar ("Aldebaran")
    Rigel       = MrKindStar ("Rigel")
    Capella     = MrKindStar ("Capella")
    Bellatrix   = MrKindStar ("Bellatrix")
    Elnath      = MrKindStar ("Elnath")
    Alnilam     = MrKindStar ("Alnilam")
    Betelgeuse  = MrKindStar ("Betelgeuse")
    Canopus     = MrKindStar ("Canopus")
    Sirius      = MrKindStar ("Sirius")
    Adhara      = MrKindStar ("Adhara")
    Procyon     = MrKindStar ("Procyon")
    Pollux      = MrKindStar ("Pollux")
    Avior       = MrKindStar ("Avior")
    Suhail      = MrKindStar ("Suhail")
    Miaplacidus = MrKindStar ("Miaplacidus")
    Alphard     = MrKindStar ("Alphard")
    Regulus     = MrKindStar ("Regulus")
    Dubhe       = MrKindStar ("Dubhe")
    Denebola    = MrKindStar ("Denebola")
    Gienah      = MrKindStar ("Gienah")
    Acrux       = MrKindStar ("Acrux")
    Gacrux      = MrKindStar ("Gacrux")
    Alioth      = MrKindStar ("Alioth")
    Spica       = MrKindStar ("Spica")
    Alkaid      = MrKindStar ("Alkaid")
    Hadar       = MrKindStar ("Hadar")
    Menkent     = MrKindStar ("Menkent")
    Arcturus    = MrKindStar ("Arcturus")
    Rigil_Kent  = MrKindStar ("Rigil Kent.")
    Kochab      = MrKindStar ("Kochab")
    Zubenubi    = MrKindStar ("Zuben'ubi")
    Alphecca    = MrKindStar ("Alphecca")
    Antares     = MrKindStar ("Antares")
    Atria       = MrKindStar ("Atria")
    Sabik       = MrKindStar ("Sabik")
    Shaula      = MrKindStar ("Shaula")
    Rasalhague  = MrKindStar ("Rasalhague")
    Eltanin     = MrKindStar ("Eltanin")
    Kaus_Aust   = MrKindStar ("Kaus Aust.")
    Vega        = MrKindStar ("Vega")
    Nunki       = MrKindStar ("Nunki")
    Altair      = MrKindStar ("Altair")
    Peacock     = MrKindStar ("Peacock")
    Deneb       = MrKindStar ("Deneb")
    Enif        = MrKindStar ("Enif")
    Al_Nair     = MrKindStar ("Al Na'ir")
    Fomalhaut   = MrKindStar ("Fomalhaut")
    Scheat      = MrKindStar ("Scheat")
    Markab      = MrKindStar ("Markab")
#pylint: enable=R0903

#pylint: disable=R0903
class ObsType:
    ''' Base for observation type taxonomy '''
    def __init__ (self, o_type : str) :
        self.o_type = o_type

    def __str__ (self) -> str:
        return self.o_type
#pylint: enable=R0903

#pylint: disable=R0903
class ObsTypes:
    ''' These are the observation types we can handle '''
    GHA = ObsType ("GHA")
    DECL = ObsType ("DECL")
    HP = ObsType ("HP")
    SHA = ObsType ("SHA")
    SD = ObsType ("SD")
#pylint: enable=R0903

#pylint: disable=R0903
class Almanac:
    ''' Represents a machine-readable almanac in pandas/csv format '''
    def __init__ (self, fn : str):
#pylint: disable=C0415
        from pandas import read_csv
#pylint: enable=C0415
        if fn in ["planets", "sun-moon", "sun-moon-sd", "venus-mars-hp"]:
            self.pd = \
            read_csv ("sample_data/"+fn + ".csv", index_col=0, delimiter=";", dtype="string")
        elif fn in ["stars"]:
            self.pd = \
            read_csv ("sample_data/"+fn + ".csv", index_col=[0,1], delimiter=";", dtype="string")
        else:
            raise NotImplementedError
        Almanac.active_almanacs [fn] = self

    active_almanacs = dict [str, object] ()

    @staticmethod
    def get_almanac (fn : str) -> object:
        ''' Return an almanac object. Use cache if possible '''
        try:
            return Almanac.active_almanacs [fn]
        except KeyError:
            return Almanac (fn)
#pylint: enable=R0903

#pylint: disable=R0912
#pylint: disable=R0914
#pylint: disable=R0915
def get_mr_item (cel_obj : MrKind | str,
                 ts : str,
                 obs_type : ObsType,
                 offset_hours : int = 0) -> str:
    ''' Get a specific item from the nautical almanac '''

    if not PANDAS_INITIALIZED:
        raise ValueError ("Pandas not available. Install it with \"pip install pandas\"")
    if isinstance (cel_obj, str):
        c2 = MrKind.get_kind (cel_obj)
        assert isinstance (c2, MrKind)
        cel_obj = c2

    if offset_hours != 0:
        if offset_hours != 1:
            raise ValueError ("offset_hours must be 0 or 1")
        x = datetime.fromisoformat (ts)
        ts = str(x + timedelta(hours=1))

    if isinstance (cel_obj, (MrKindPlanet, MrKindAries)):
        if str(obs_type) in ["HP"]:
            the_almanac = Almanac.get_almanac ("venus-mars-hp")
            df = the_almanac.pd

            ready = False
            ts_dt = datetime.fromisoformat (ts)
            day_d = date (year=ts_dt.year, month=ts_dt.month, day=ts_dt.day)
            iter_count = 0
            max_iter = 4
            loc = None
            while not ready:
                day_d_s = str(day_d)
                try:
                    loc = df.loc [day_d_s]
                    ready = True
                except KeyError as ke:
                    day_d = day_d + timedelta (days=-1)
                    iter_count += 1
                    if iter_count > max_iter:
                        raise ValueError ("Database match error") from ke
            try:
#pylint: disable=C0415
                from pandas import Series
#pylint: enable=C0415
                assert isinstance (loc, Series)
                return str(loc[str(cel_obj)+"_"+str(obs_type)])
            except KeyError as ie:
                raise ValueError ("Invalid parameter") from ie

        else:
            the_almanac = Almanac.get_almanac ("planets")
            df = the_almanac.pd
            loc = df.loc[ts]
            try:
                return str(loc[str(cel_obj)+"_"+str(obs_type)])
            except KeyError as ie:
                raise ValueError ("Invalid parameter") from ie
    elif isinstance (cel_obj, MrKindCentral):
        if str(obs_type) in ["SD","v"]:
            the_almanac = Almanac.get_almanac ("sun-moon-sd")
            df = the_almanac.pd
            ts_dt = datetime.fromisoformat (ts)
            day_d = date (year=ts_dt.year, month=ts_dt.month, day=ts_dt.day)
            day_d_s = str(day_d)
            loc = df.loc[day_d_s]
            try:
                return str(loc[str(cel_obj)+"_"+str(obs_type)])
            except KeyError as ie:
                raise ValueError ("Invalid parameter") from ie
        else:
            the_almanac = Almanac.get_almanac ("sun-moon")
            df = the_almanac.pd
            loc = df.loc[ts]
            try:
                return str(loc[str(cel_obj)+"_"+str(obs_type)])
            except KeyError as ie:
                raise ValueError ("Invalid parameter") from ie
    elif isinstance (cel_obj ,MrKindStar):
        if str(obs_type) in ["GHA"]:
            return get_mr_item ("Aries", ts, ObsTypes.GHA)
        the_almanac = Almanac.get_almanac ("stars")
        df = the_almanac.pd
        ready = False
        ts_dt = datetime.fromisoformat (ts)
        day_d = date (year=ts_dt.year, month=ts_dt.month, day=ts_dt.day)
        iter_count = 0
        max_iter = 4
        loc = None
        while not ready:
            day_d_s = str(day_d)
            try:
                loc = df.loc [day_d_s,str(cel_obj)]
                ready = True
            except KeyError as ke:
                day_d = day_d + timedelta (days=-1)
                iter_count += 1
                if iter_count > max_iter:
                    raise ValueError ("Database match error") from ke
        try:
#pylint: disable=C0415
            from pandas import Series
#pylint: enable=C0415
            assert isinstance (loc, Series)
            return str(loc[str(obs_type)])
        except KeyError as ie:
            raise ValueError ("Invalid parameter") from ie
    raise NotImplementedError ()
#pylint: enable=R0912
#pylint: enable=R0914
#pylint: enable=R0915

################################################
# Celestial Navigation
################################################

#pylint: disable=R0902
class Sight :
    '''  Object representing a sight (star fix) '''

    # This is a cached value for the estimated_position parameter
    estimated_position_hold = None
    alt_diff_hold           = 0.0
    time_diff_hold          = 0.0

    @staticmethod
    def set_estimated_position (drp : LatLon):
        ''' Set the estimated position value (DRP) '''
        Sight.estimated_position_hold = drp

    @staticmethod
    def set_alt_diff (alt_diff : float):
        ''' Set the alt sigma (used in Monte Carlo simulation) '''
        Sight.alt_diff_hold = alt_diff

    @staticmethod
    def set_time_diff (time_diff : float):
        ''' Set the time sigma (used in Monte Carlo simulations) '''
        Sight.time_diff_hold = time_diff

    MR_DEBUG = False

    # Used as special values for SD correction (limb correction)
    LIMB_LOWER = -1
    LIMB_CENTRAL = 0
    LIMB_UPPER = 1

#pylint: disable=R0912
#pylint: disable=R0913
#pylint: disable=R0914
    def __init__ (self, \
                  object_name              : str,
                  set_time                 : str,
                  measured_alt             : str,
                  gha_time_0               : str | NoneType = None,
                  gha_time_1               : str | NoneType = None,
                  decl_time_0              : str | NoneType = None,
                  decl_time_1              : NoneType | str = None,
                  estimated_position       : LatLonGeodetic | NoneType = None,
                  sha_diff                 : NoneType | str = None,
                  observer_height          : int | float = 0,
                  artificial_horizon       : bool = False,
                  index_error_minutes      : int | float = 0,
                  limb_correction          : int = 0,
                  horizontal_parallax      : int | float | NoneType = None,
                  sextant                  : NoneType | Sextant = None,
                  chronometer              : NoneType | Chronometer = None,
                  temperature              : float = 10.0,
                  dt_dh                    : float = -0.01,
                  pressure                 : float = 101.0,
                  ho_obs                   : bool = False,
                  no_dip                   : bool = False):               # For MC simulation

        def q_replace (x : datetime) -> datetime:
            p = x
            q = p.astimezone (timezone.utc)
            q = q.replace (tzinfo=None)
            return q

        self.temperature          = temperature
        self.dt_dh                = dt_dh
        self.pressure             = pressure
        self.__object_name        = object_name
        self.__set_time_dt        = datetime.fromisoformat (set_time)
        self.set_time_dt_hour     = self.__set_time_dt.replace\
                                      (second=0, microsecond=0, minute=0,
                                       hour=self.__set_time_dt.hour,\
                                       tzinfo=self.__set_time_dt.tzinfo)
        if Sight.time_diff_hold != 0.0:
            diff = gauss(0, Sight.time_diff_hold)
            new_time = self.get_time() + timedelta(seconds=diff)
            self.set_time_dt = new_time
        if gha_time_0 is None:

            gha_time_0 = get_mr_item (self.get_object_name(),
                                      str(q_replace(self.set_time_dt_hour)),
                                      ObsTypes.GHA)
            if Sight.MR_DEBUG:
                print ("GHA_0 = " + gha_time_0)
        self.gha_time_0           = parse_angle_string (gha_time_0)
        if gha_time_1 is None:

            gha_time_1 = get_mr_item (self.get_object_name(),
                                      str(q_replace(self.set_time_dt_hour)),
                                      ObsTypes.GHA,
                                      offset_hours=1)
            if Sight.MR_DEBUG:
                print ("GHA_1 = " + gha_time_1)
        self.gha_time_1           = parse_angle_string (gha_time_1)
        if self.gha_time_1 < self.gha_time_0:
            self.gha_time_1 += 360
        if decl_time_1 is None:
            decl_time_1 = decl_time_0
        if decl_time_0 is None:

            decl_time_0 = get_mr_item (self.get_object_name(),
                                      str(q_replace(self.set_time_dt_hour)),
                                      ObsTypes.DECL)
            if Sight.MR_DEBUG:
                print ("DECL_0 = " + decl_time_0)
        self.decl_time_0          = parse_angle_string (decl_time_0)
        if decl_time_1 is None:

            decl_time_1 = get_mr_item (self.get_object_name(),
                                      str(q_replace(self.set_time_dt_hour)),
                                      ObsTypes.DECL,
                                      offset_hours=1)
            if Sight.MR_DEBUG:
                print ("DECL_1 = " + decl_time_1)
        self.decl_time_1          = parse_angle_string (decl_time_1)
        if self.decl_time_0 < -90 or self.decl_time_0 > 90 or \
           self.decl_time_1 < -90 or self.decl_time_1 > 90:
            raise ValueError ("Declination values must be within [-90,90]")
        self.measured_alt         = parse_angle_string (measured_alt)
        if Sight.alt_diff_hold != 0.0:
            diff                  = gauss (0, Sight.alt_diff_hold) / 60
            self.measured_alt     += diff
            # Take care if the altitude extends outside [0,90]
            if self.measured_alt < 0:
                self.measured_alt = 0
            if self.measured_alt >= 90:
                self.measured_alt = 89.999999
        if sha_diff is not None:
            self.sha_diff         = parse_angle_string (sha_diff)
        elif MrKindStar.is_star (self.get_object_name()):
            qq = get_mr_item (self.get_object_name(),
                                str(q_replace(self.set_time_dt_hour)),
                                ObsTypes.SHA)
            if Sight.MR_DEBUG:
                print ("SHA = " + qq)
            self.sha_diff = parse_angle_string (qq)
        else:
            self.sha_diff         = 0
        self.observer_height      = observer_height
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
        if self.measured_alt < 0 or self.measured_alt >= 90:
            raise ValueError ("Altitude value must be within (0,90]")

        if limb_correction == Sight.LIMB_CENTRAL:
            semi_diameter_correction = 0
        elif limb_correction in [Sight.LIMB_LOWER,Sight.LIMB_UPPER]:
            if self.get_object_name() in ["Sun", "Moon"]:
                qq = get_mr_item (self.get_object_name(),
                                  str(q_replace(self.set_time_dt_hour)),
                                  ObsTypes.SD)
                q = float (qq)
                semi_diameter_correction = -1 * limb_correction * q
            else:
                semi_diameter_correction = 0
        else:
            raise ValueError ("limb_correction must be one of -1,0 or 1")
        if semi_diameter_correction != 0:
            self.__correct_semi_diameter (semi_diameter_correction)
        if horizontal_parallax is None:
            if self.get_object_name() == "Moon":
                qq = get_mr_item (self.get_object_name(),
                                  str(q_replace(self.set_time_dt_hour)),
                                  ObsTypes.HP)
                if Sight.MR_DEBUG:
                    print ("HP = " + qq)
                horizontal_parallax = 60 * parse_angle_string (qq)
            else:
                horizontal_parallax = 0
        if horizontal_parallax != 0:
            self.__correct_for_horizontal_parallax (horizontal_parallax)
        if not ho_obs:
            self.__correct_for_refraction ()
            if not no_dip:
                self.__correct_dip_of_horizon ()
        self.gp = self.__calculate_gp ()

        if estimated_position is None:
            # Use previously used parameter value
            if Sight.estimated_position_hold is None:
                raise ValueError ("A DRP (Estimated position) is needed!")
            self.estimated_position = Sight.estimated_position_hold
        else:
            self.estimated_position = estimated_position

        # Saving the specified estimated position for later use (calls with no parameter specified)
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

    def get_object_name (self) -> str:
        ''' Returns the object name (celestial object name) of the sight '''
        return self.__object_name

    def get_time (self) -> datetime:
        ''' Returns the timestamp of this sight '''
        return self.__set_time_dt

    def __correct_set_time (self, chronometer : Chronometer):
        dt1 = self.set_time_dt
        dt2 = chronometer.get_corrected_time (dt1)
        self.set_time_dt = dt2

    def __correct_for_error (self, sextant : Sextant):
        #self.measured_alt /= sextant.graduation_error
        #self.measured_alt -= sextant.index_error/60
        self.measured_alt -= sextant.index_error/60
        self.measured_alt /= sextant.graduation_error
        # Proposed change. See https://github.com/alinnman/celestial-navigation/discussions/3
        # TODO Review this.

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

    def __calculate_gp (self) -> LatLonGeocentric:
        min_sec_contribution = (self.__set_time_dt - self.set_time_dt_hour).total_seconds() / 3600

        result_lon = mod_lon (- \
        ((self.gha_time_0 + self.sha_diff) + \
        ((self.gha_time_1 - self.gha_time_0))*min_sec_contribution))

        result_lat = \
        self.decl_time_0 + (self.decl_time_1 - self.decl_time_0)*min_sec_contribution

        return LatLonGeocentric (result_lat, result_lon)

    def get_angle (self, geodetic : bool) -> float:
        ''' Returns the (Earth-based) angle of the sight '''
        if geodetic:
            return 90-self.raw_measured_alt
        return 90-self.measured_alt

    def get_circle (self, geodetic : bool) -> Circle:
        ''' Return a circle object corresponding to this Sight '''
        circumference = EARTH_CIRCUMFERENCE
        if geodetic:
            gp_x = LatLonGeodetic (ll = self.gp)
        else:
            gp_x = self.gp
        retval = Circle (gp_x, self.get_angle(geodetic=geodetic),\
                         circumference)
        return retval

    def get_distance_from (self, p : LatLonGeocentric, geodetic : bool) -> float:
        ''' Return the spherical distance from point (p) to the sight circle of equal altitude '''
        p_distance = spherical_distance (p, self.gp)
        the_radius = self.get_circle(geodetic=geodetic).get_radius ()
        return p_distance - the_radius

    def get_azimuth (self, from_pos : LatLon) -> float:
        ''' Return the azimuth of this sight (to the GP) from a particular point on Earth 
            Returns the azimuth in degrees (0-360)'''
        return get_azimuth (self.gp, from_pos)

    def render_folium (self, the_map : object, draw_markers = True):
        ''' Render this Sight object on a Folium Map object'''

        check_folium ()

        the_object_name = self.get_object_name()
        #assert isinstance (s, Sight)
        c = self.get_circle (geodetic=False)
        c_latlon = c.get_latlon()
        c_latlon_d = LatLonGeodetic (ll = c_latlon)
        time_string = str(self.get_time())

#pylint: disable=C0415
        from folium import Map, Marker, Icon
#pylint: enable=C0415
        assert isinstance (the_map, Map)
        # Set a marker for a GP
        if draw_markers:
            Marker(
                location=[c_latlon_d.get_lat(), c_latlon_d.get_lon()],
                tooltip=the_object_name,
                popup=the_object_name + "\n" + time_string + "\n" + str(c_latlon_d),
                icon=Icon(icon="star"),
            ).add_to(the_map)

        c.render_folium (the_map)

#pylint: enable=R0902

#pylint: disable=R0903
class SightPair:
    ''' Represents a pair of sights, needed for making a sight reduction '''
    def __init__ (self, sf1 : Sight, sf2 : Sight):
        self.sf1 = sf1
        self.sf2 = sf2

    def get_intersections\
                      (self, return_geodetic : bool,
                       estimated_position : NoneType | LatLon = None,
                       diagnostics : bool = False,
                       intersection_number : int = 0) ->\
                       tuple[LatLonGeocentric | tuple[LatLonGeocentric, LatLonGeocentric],
                             float, str]:
        ''' Return the two intersections for this sight pair. 
            The parameter estimated_position can be used to eliminate the false intersection '''

        circle1 = self.sf1.get_circle (geodetic = return_geodetic)
        circle2 = self.sf2.get_circle (geodetic = return_geodetic)
        retval = get_intersections (circle1, circle2,
                                estimated_position=estimated_position,\
                                diagnostics = diagnostics,
                                intersection_number = intersection_number)
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
          assume_good_estimated_position = True,
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
            try:
                intersections, fitness, diag_output =\
                    SightPair (self.sf_list[0],\
                                self.sf_list[1]).get_intersections\
                                            (return_geodetic=False,
                                            estimated_position=estimated_position,\
                                            diagnostics = diagnostics)
            except IntersectError as ie:
                raise IntersectError (str(ie), self) from ie

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
        coords = list[tuple[LatLonGeocentric, float]]()
        # Perform pairwise sight reductions
        intersection_count = 0
        for i in range (nr_of_fixes):
            for j in range (i+1, nr_of_fixes):
                p = SightPair (self.sf_list [i], self.sf_list [j])
                intersection_count += 1
                try:
                    if assume_good_estimated_position:
                        ep = estimated_position
                    else:
                        ep = None
                    p_int, fitness, dia =\
                        p.get_intersections (return_geodetic=False,
                                             estimated_position=ep,
                                             diagnostics = diagnostics,\
                                             intersection_number = intersection_count)
                except IntersectError as ie:
                    raise IntersectError (str(ie), self) from ie
                diag_output += dia
                if p_int is not None:
                    if isinstance (p_int, (list, tuple)):
                        for pix in p_int:
                            coords.append ((pix, fitness))
                    elif isinstance (p_int, LatLonGeocentric):
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
            diag_output += "|"
            for i in range (nr_of_coords):
                diag_output += "|" + str(i)
            diag_output += "|\n"
            diag_output += "|----"
            for i in range (nr_of_coords):
                diag_output += "|----"
            diag_output += "|\n"
        for i in range (nr_of_coords):
            if diag_output:
                diag_output += "|**" + str(i) + "**"
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
            raise IntersectError ("Bad sight data.", self)

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
                                "a reasonable set of coordinates", self)

        summation_vec = [0.0,0.0,0.0]
        # Make a mean value on the best intersections.
        fitness_sum = 0
        for cp in chosen_points:
            selected_coord = coords [cp][0]
            penalty_coefficient = 1
            fitness_here = coords [cp][1]**penalty_coefficient # Penalize bad intersections
            fitness_sum += fitness_here
            rect_vec = to_rectangular (selected_coord)
            summation_vec =\
                add_vecs (summation_vec,\
                mult_scalar_vect ((1/nr_of_chosen_points)*fitness_here, rect_vec))
        summation_vec = normalize_vect (summation_vec)
        ret_latlon = to_latlon (summation_vec)
        if return_geodetic:
            return LatLonGeodetic(ll=ret_latlon), fitness_sum, diag_output
        return ret_latlon, fitness_sum, diag_output
#pylint: enable=R0912
#pylint: enable=R0914
#pylint: enable=R0915

#pylint: disable=R0913
#pylint: disable=R0914
#pylint: disable=R0917
    @staticmethod
    def get_intersections_mc\
         (return_geodetic : bool,
            estimated_position : LatLon,
            get_starfixes : Callable,
            limit : int | float = 100,
            alt_sigma : float = 0.0,
            time_sigma : float = 0.0,
            max_mc_iter : int = 1) -> tuple [LatLon, float, int]:
        '''
        Calculate intersections based on monte carlo (random)
        simulations with errors/deviations in measured angle and time.
        This function can be used to get an approximation of the 
        inaccuracy of the intersection algorithm. 
        '''
        if alt_sigma < 0.0 or time_sigma < 0.0:
            raise ValueError ("Sigma parameter must be >= 0.0")
        if max_mc_iter < 1:
            raise ValueError ("max_mc_iter must be >= 1")
        # Perform Monte Carlo Simulation
        sum_rect = [0.0,0.0,0.0]
        int_coll = list [LatLon] ()
        found_intersections = 0
        for _ in range(max_mc_iter):
            # Perform one perturberated intersection
            sc = get_starfixes (estimated_position, alt_sigma, time_sigma)
            assert isinstance (sc, SightCollection)
            intersections = None
            try:
                intersections, _, _ = \
                sc.get_intersections (return_geodetic=return_geodetic,
                                      limit=limit,
                                      estimated_position=estimated_position,
                                      diagnostics=False)
                found_intersections += 1
            except IntersectError:
                # Ignore failed intersections. Larger deviations will cause
                # the intersections to fail.
                pass
            if intersections is not None:
                # Collect the data
                assert isinstance (intersections, LatLon)
                rect1 = to_rectangular (intersections)
                sum_rect = add_vecs (sum_rect, rect1)
                int_coll.append (intersections)

        if found_intersections == 0:
            # At least ONE intersection should be found
            raise IntersectError ("Cannot work on intersections for this MC set.")

        sum_rect = mult_scalar_vect (1/found_intersections, sum_rect)
        intersections = to_latlon (sum_rect)
        # Convert this latlon to geodetic, since it IS geodetic...
        intersections = LatLonGeodetic (lat=intersections.get_lat(),\
                                        lon=intersections.get_lon())

        square_sum = 0.0
        for c in int_coll:
            sd = spherical_distance (intersections, c)
            sd = sd*sd
            square_sum += sd
        square_sum /= found_intersections
        sigma = sqrt (square_sum)
        return intersections, sigma, found_intersections
#pylint: enable=R0913
#pylint: enable=R0914
#pylint: enable=R0917

#pylint: disable=R0913
#pylint: disable=R0917
#pylint: disable=R0914
    @staticmethod
    def get_intersections_conv\
        (return_geodetic : bool,
            estimated_position : LatLon,
            get_starfixes : Callable,
            assume_good_estimated_position : bool = True,
            limit : int | float = 100,
            diagnostics : bool = False,
            max_iter : int = 10,
            dist_limit : float = 0.01) ->\
            tuple[LatLon | tuple[LatLon, LatLon], float, str, object]:
        ''' Returns an intersection based on improved algorithm.
            Successively searches for (iterates) to get the correct
            position. Each iteration improves the DRP (using the result
            of the previous iteration)
        '''
        ready = False
        intersections = None
        collection = None
        fitness = None
        diag = None
        counter = 0
        while not ready:
            # This loop will repeat the sight reduction with successively more
            # accurate DR positions
            collection = get_starfixes (estimated_position)
            assert isinstance (collection, SightCollection)
            intersections, fitness, diag =\
            collection.get_intersections (return_geodetic=return_geodetic,
                                          limit=limit,
                                          diagnostics=diagnostics,
                                          assume_good_estimated_position=\
                                          assume_good_estimated_position)
            assert isinstance (intersections, LatLon)
            the_distance = spherical_distance (estimated_position, intersections)
            if the_distance < dist_limit:
                ready = True
            else:
                estimated_position = intersections
            counter += 1
            if counter >= max_iter:
                raise IntersectError ("Cannot find an intersection. Bad data?")
        assert intersections is not None
        assert fitness is not None
        assert diag is not None
        return intersections, fitness, diag, collection
#pylint: enable=R0913
#pylint: enable=R0917
#pylint: enable=R0914

#pylint: disable=R0914
    def render_folium\
          (self, intersections : tuple [LatLon, LatLon] | LatLon | NoneType = None,\
           accuracy : float = 1000, label_text = "Intersection",
           draw_grid = True, draw_markers = True) -> object:
        ''' Renders a folium object (Map) to be used for map plotting'''

        check_folium ()
        the_sf_list = self.sf_list

#pylint: disable=C0415
        from folium import Map, Circle as Folium_Circle, PolyLine, Marker, Icon
#pylint: enable=C0415

        if isinstance (intersections, LatLon):
            int_geodetic = LatLonGeodetic (ll=intersections.get_latlon())

            the_map = Map(location=(int_geodetic.get_lat(),\
                                    int_geodetic.get_lon()), zoom_start=12)

            radius = accuracy
            Folium_Circle(
                location=[int_geodetic.get_lat(),\
                        int_geodetic.get_lon()],
                radius=radius,
                color="black",
                weight=1,
                fill_opacity=0.6,
                opacity=1,
                fill_color="lightgreen",
                fill=False,  # gets overridden by fill_color
                popup = "Radius = " + str(radius) + " meters",
                tooltip="Radius : " + str(accuracy) + " m."
            ).add_to(the_map)
            if draw_markers:
                Marker(
                    location=[int_geodetic.get_lat(), int_geodetic.get_lon()],
                    tooltip=label_text,
                    popup= label_text + " " + str (intersections),
                    icon=Icon(icon="user"),
                ).add_to(the_map)
        else:
            the_map = Map(location=(0,\
                                    0), zoom_start=6)

        for s in the_sf_list:
            s.render_folium (the_map, draw_markers=draw_markers)

        if draw_grid:

            lat_interval = 1
            lon_interval = 1

            if isinstance (intersections, LatLon):
                left_lon = int(intersections.get_lon() - 180)
                right_lon = int(intersections.get_lon() + 181)
            else:
                left_lon = -180
                right_lon = 181

            for lat in range(-90, 91, lat_interval):
                PolyLine([[lat, left_lon],[lat, right_lon]], weight=0.5, tooltip=str(lat)).\
                    add_to(the_map)

            for lon in range(left_lon, right_lon, lon_interval):
                PolyLine([[-90, lon],[90, lon]], weight=0.5, tooltip=str(lon)).\
                    add_to(the_map)

        return the_map
#pylint: enable=R0914

#pylint: disable=R0902
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
#pylint: enable=R0913

    def __calculate_time_hours (self):
        if isinstance (self.sight_start, Sight):
            dt1 = self.sight_start.get_time()
        else:
            dt1 = self.sight_start
        dt2 = self.sight_end.get_time()
        self.time_hours = calculate_time_hours (dt1, dt2)

    def __calculate_distance_to_target (self, angle : int | float,
                                        a_vec : list [float], b_vec : list [float])\
          -> tuple [float, LatLonGeocentric, LatLonGeocentric]:
        rotation_angle = deg_to_rad (angle)
        rotated_vec = rotate_vector (b_vec, a_vec, rotation_angle)
        rotated_latlon = to_latlon (rotated_vec)
        taken_out = takeout_course (rotated_latlon, self.course_degrees,\
                                   self.speed_knots, self.time_hours)

        dbp = spherical_distance\
              (taken_out, self.sight_end.gp)\
                  - self.sight_end.get_circle(geodetic=False).get_radius()
        return dbp, taken_out, rotated_latlon

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
            assert isinstance (best_intersection, LatLonGeocentric)
            b_vec = to_rectangular (best_intersection)

            # Apply Newtons method to find the location
            current_rotation = 0
            delta = 0.0001
            limit = 0.001
            iter_limit = 100
            iter_count = 0
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
        assert isinstance (taken_out, LatLonGeocentric)
        circle1 = Circle (self.sight_end.gp,
                          self.sight_end.get_angle(geodetic = False),
                          EARTH_CIRCUMFERENCE)

        circle2 = get_great_circle_route (taken_out, self.sight_end.gp)

        assert isinstance (circle2, Circle)
        self.movement_vec = circle2.get_latlon()
        gi, fitness, diag = get_intersections \
                           (circle1, circle2,
                            estimated_position=taken_out)

        assert isinstance (gi, LatLonGeocentric)
        self.start_pos = self.estimated_starting_point
        self.end_pos = gi
        if return_geodetic:
            gi = LatLonGeodetic (ll=gi)
        return gi, fitness, diag
#pylint: enable=R0914

    def render_folium (self, intersections : tuple [LatLon, LatLon] | LatLon,\
                       accuracy : float = 1000, draw_grid = True, draw_markers = True):
        ''' Renders this object as a Folium Map object '''

        check_folium ()

#pylint: disable=C0415
        from folium import Map, Marker, PolyLine, Icon, Circle as Folium_Circle
#pylint: enable=C0415

        def draw_arrow (m : Map, from_point : LatLon, to_point : LatLon):
            PolyLine (
                locations=[[from_point.get_lat(), from_point.get_lon()],
                           [to_point.get_lat(),   to_point.get_lon()]]
            ).add_to(m)

        if isinstance (self.sight_start, Sight):
            assert isinstance (intersections, tuple)
            s_c = SightCollection ([self.sight_start, self.sight_end])
            retval = s_c.render_folium (intersections=intersections[0],\
                                        accuracy=accuracy,\
                                        label_text="Target",\
                                        draw_grid=draw_grid)
            assert isinstance (retval, Map)
            if draw_markers:
                Marker (icon=Icon(color='lightgray', icon='home', prefix='fa'),
                        tooltip = "Starting point",
                        popup = "Starting point " + str(intersections[1]),
                        location=[intersections[1].get_lat(),\
                                intersections[1].get_lon()]).add_to(retval)
            draw_arrow (retval, intersections [1], intersections [0])
            return retval

        assert isinstance (self.movement_vec, LatLonGeocentric)
        assert isinstance (self.start_pos, LatLon)
        assert isinstance (self.end_pos, LatLon)
        end_pos_d   = LatLonGeodetic (ll = self.end_pos)
        draw_map = Map (location = [end_pos_d.get_lat(),\
                                    end_pos_d.get_lon()])
        self.sight_end.render_folium (draw_map)


        # Handle/plot markers
        if isinstance (self.start_pos, LatLonGeocentric) and \
           isinstance (self.end_pos, LatLonGeocentric):
            start_pos_d = LatLonGeodetic (ll = self.start_pos)
            if draw_markers:
                Marker (icon=Icon(color='lightgray', icon='home', prefix='fa'),
                        tooltip = "Starting point",
                        popup = "Starting point " + str(start_pos_d),
                        location=[start_pos_d.get_lat(),\
                                start_pos_d.get_lon()]).add_to(draw_map)
            end_pos_d = LatLonGeodetic (ll = self.end_pos)
            Folium_Circle (location = [end_pos_d.get_lat(), end_pos_d.get_lon()],
                           radius=accuracy).add_to (draw_map)
            if draw_markers:
                Marker (icon=Icon(color='blue', icon='user', prefix='fa'),
                        tooltip = "Target",
                        popup = "Target " + str(end_pos_d),
                        location=[end_pos_d.get_lat(),\
                                end_pos_d.get_lon()]).add_to(draw_map)
            draw_arrow (draw_map, start_pos_d, end_pos_d)

        return draw_map

#pylint: enable=R0902
