''' Simple sample representing a trip at sea with supporting celestial navigation
    © August Linnman, 2024, email: august@linnman.net
    MIT License (see LICENSE file)       
'''

from time import time
from starfix import LatLonGeodetic, get_representation,\
                    get_great_circle_route, Circle, CircleCollection, get_intersections,\
                    get_line_of_sight, nm_to_km, km_to_nm, EARTH_CIRCUMFERENCE
def main ():
    ''' Main body of script '''

    starttime = time ()

    # We are sailing from point s1
    # We have a good estimate of an initial position. (A previous fix)
    s1 = LatLonGeodetic (57.662, 18.263)
    s1_gc = s1.get_latlon ()
    # We start out at a course of 350 degrees
    c_course = 350
    course_gc = get_great_circle_route (s1_gc,
                                        # NOTE: The s1 coordinate must be converted to geocentrical
                                        c_course)

    # This is a position of a lighthouse
    light_house = LatLonGeodetic (58.739, 17.865)
    light_house_gc = light_house.get_latlon ()
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

    light_house_circle_gc = Circle\
          (light_house_gc, actual_line_of_sight_nm/60, circumference=EARTH_CIRCUMFERENCE)

    print ("--------- Sight Reduction  --------- ")
    course_gc.make_geodetic()
    intersections = get_intersections (course_gc, light_house_circle_gc) # , estimated_position=s1)
    endtime = time ()
    assert isinstance (intersections, tuple)
    #print (get_representation(intersections[0],1))
    f = intersections [0]
    assert isinstance (f, tuple)
    intersection_circles = list [Circle] ()    
    for i in range(2):
        the_coord = LatLonGeodetic(ll=f[i])
        print (get_representation(the_coord,1))
        intersection_circles.append (Circle (the_coord, 1/60, circumference=EARTH_CIRCUMFERENCE))

    print ("--------- Mapping          --------- ")
    origin_circle = Circle(s1, 1/60, circumference=EARTH_CIRCUMFERENCE).make_geodetic()
    light_house_circle = light_house_circle_gc.make_geodetic ()
    c_c = CircleCollection ([light_house_circle,
                             intersection_circles[0],
                             intersection_circles[1],
                             origin_circle])
    print (c_c.get_map_developers_string())

    taken_ms = round((endtime-starttime)*1000,2)

    print ("Time taken = " +str(taken_ms)+" ms")

if __name__ == '__main__':
    main()
