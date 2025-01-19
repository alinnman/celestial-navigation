''' Simple sample representing a trip at sea with supporting celestial navigation
    © August Linnman, 2024, email: august@linnman.net
    MIT License (see LICENSE file)       
'''

from time import time
from starfix import LatLon, get_representation,\
                    get_great_circle_route, Circle, CircleCollection, get_intersections,\
                    get_line_of_sight, nm_to_km, km_to_nm, EARTH_CIRCUMFERENCE
def main ():
    ''' Main body of script '''

    starttime = time ()

    # We are sailing from point s1
    # We have a good estimate of an initial position. (A previous fix)
    s1 = LatLon (57.662, 18.263)
    # We start out at a course of 350 degrees
    c_course = 350
    course_gc = get_great_circle_route (s1,
                                        # NOTE: The s1 coordinate must be converted to geocentrical
                                        c_course)

    # This is a position of a lighthouse
    light_house = LatLon (58.739, 17.865)
    # This is the elevation of the light source (m)
    light_house_elevation = 44.5
    # This is the maximum reach in nm
    light_house_max_visibility_nm = 22
    light_house_max_visibility_m = nm_to_km (light_house_max_visibility_nm) * 1000
    # This is the elevation of the observer (in the ship)
    observer_elevation = 3
    # Calculate the max line of sight
    line_of_sight = get_line_of_sight (light_house_elevation, observer_elevation)
    # The actual line of sight is the minimum of max reach and line of sight
    actual_line_of_sight = min (line_of_sight, light_house_max_visibility_m)
    actual_line_of_sight_nm = km_to_nm (actual_line_of_sight/1000)

    light_house_circle = Circle\
          (light_house, actual_line_of_sight_nm/60, circumference=EARTH_CIRCUMFERENCE)

    # Get the intersections
    #course_gc.make_geodetic() # TODO Review
    intersections = get_intersections (course_gc, light_house_circle)
    endtime = time ()
    assert isinstance (intersections, tuple)
    print (get_representation(intersections[0],1))

    # Check the circles on the map
    c_c = CircleCollection ([course_gc, light_house_circle,\
                              Circle(s1, 1/60, circumference=EARTH_CIRCUMFERENCE)])
    # c_c.make_geodetic () # Geodetic coordinates needed here # TODO Review
    print ("MD = " + c_c.get_map_developers_string())

    taken_ms = round((endtime-starttime)*1000,2)

    print ("Time taken = " +str(taken_ms)+" ms")

if __name__ == '__main__':
    main()
